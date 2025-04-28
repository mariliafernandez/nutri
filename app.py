from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Literal

from src.Meal import Meal
from src.Database import Database
from src.FoodItem import FoodItem
from src.InsulinCounter import InsulinCounter
from dotenv import load_dotenv

import os


load_dotenv()

description = """
A **NutrinionALL API** facilita o acesso a informações nutricionais de alimentos e permite a integração de dados nutricionais em sua aplicação de forma simples e eficiente. Oferecemos uma solução completa para:

- Informações nutricionais de bases brasileiras consolidadas e integradas em um único lugar:
    - TACO (Tabela Brasileira de Composição de Alimentos)
    - IBGE (Instituto Brasileiro de Geografia e Estatística)
- Consulta de informações nutricionais de alimentos de forma rápida e customizada
- Cálculo personalizado de:
  - Macronutrientes
  - Calorias
  - Necessidades de insulina

Desenvolvida para aplicações de **saúde**, **nutrição** e **controle glicêmico**, a API permite integrações fáceis e rápidas por meio de **endpoints RESTful**.

"""

app = FastAPI(
    title="NutritionALL API",
    version="1.0.0",
    description=description,
    openapi_tags=None,
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
)


class SearchItem(BaseModel):
    name: str | None = None
    order_by: str | None = None
    ascending: bool | None = None
    max_results: int | None = None
    categories: list[str] = []


class RelationItem(BaseModel):
    col1: Literal["energy_kcal", "protein_g", "lipid_g", "carbohydrate_g", "fiber_g"]
    col2: Literal["energy_kcal", "protein_g", "lipid_g", "carbohydrate_g", "fiber_g"]
    ascending: bool = False
    max_results: int | None = None
    categories: list[str] = []


class FoodPortion(BaseModel):
    food_id: int
    grams: int


class MealInput(BaseModel):
    meal: list[FoodPortion]
    factor_insulin_cho: int = None
    mode: Literal["carbo", "fpi", "fpu"] = "carbo"


class FoodItemResponse(BaseModel):
    id: int
    description: str
    category: str
    energy_kcal: float | None
    protein_g: float | None
    lipid_g: float | None
    carbohydrate_g: float | None
    fiber_g: float | None
    source: Literal["taco", "ibge"]
    grams: int = 100


class RelationItemResponse(BaseModel):
    id: int
    description: str
    category: str
    energy_kcal: float | None
    protein_g: float | None
    lipid_g: float | None
    carbohydrate_g: float | None
    fiber_g: float | None
    relation_value: float | None
    relation_description: str
    source: Literal["taco", "ibge"]
    grams: int = 100


class RelationResponse(BaseModel):
    items: list[RelationItemResponse]


class CollectionResponse(BaseModel):
    items: list[FoodItemResponse]


class CalculateResponse(BaseModel):
    energy_kcal: float
    carbohydrate_g: float
    protein_g: float
    lipid_g: float
    fiber_g: float
    insulin_needed: float | None


@app.get("/api/health", name="Health Check", tags=["Endpoints"])
def health_check():
    """Verifica a saúde do serviço e a conexão com o banco de dados."""
    try:
        # Fazendo uma consulta simples no banco para verificar a conexão
        with Database(url=os.getenv("DB_URL")) as connection:
            result = connection.run_query("SELECT 1")
    except Exception as e:
        return JSONResponse(
            status_code=503, content={"status": "nok", "db_error": str(e)}
        )

    if len(result) == 1:
        return JSONResponse(status_code=200, content={"status": "ok"})

    return JSONResponse(status_code=200, content={"status": "nok"})


@app.get("/api/categories", name="Categorias Disponíveis", tags=["Endpoints"])
def get_categories():
    """Retorna as categorias disponíveis no banco de dados."""
    with Database(url=os.getenv("DB_URL")) as db:
        categories = db.select(
            table_name="integrate_tables",
            columns="category",
            distinct=True,
        )

    return {"categories": [cat["category"] for cat in categories]}


@app.post("/api/search", name="Consulta de Alimentos", tags=["Endpoints"])
def search(item: SearchItem):
    """
    Consulta de alimentos com base nos parâmetros fornecidos.
    """
    with Database(url=os.getenv("DB_URL")) as db:
        result = db.select(
            table_name="integrate_tables",
            description_like=item.name,
            categories=item.categories,
            order_by=item.order_by,
            order="ASC" if item.ascending else "DESC",
            limit=item.max_results,
        )

    return CollectionResponse(items=result)


@app.post(
    "/api/relation", name="Consulta por Relações Nutricionais", tags=["Endpoints"]
)
def relation(item: RelationItem):
    """
    Lista os alimentos com base na relação nutricional entre dois parâmetros `("energy_kcal", "protein_g", "lipid_g", "carbohydrate_g", "fiber_g")`.
    """
    with Database(url=os.getenv("DB_URL")) as db:
        results = db.select_relation(
            table_name="integrate_tables",
            select_columns="id, description, category, energy_kcal, protein_g, lipid_g, carbohydrate_g, fiber_g, source",
            col1=item.col1,
            col2=item.col2,
            categories=item.categories,
            order="ASC" if item.ascending else "DESC",
            limit=item.max_results,
        )

    results = [
        r | {"relation_description": f"{item.col1} / {item.col2}"} for r in results
    ]

    return RelationResponse(items=results)


@app.post(
    "/api/calculate", name="Cálculo de Macronutrientes e Insulina", tags=["Endpoints"]
)
def calculate(meal_input: MealInput):
    """
    Calcula os macronutrientes totais de uma refeição com base nos alimentos e suas quantidades em gramas e a quantidade de insulina necessária (opcional) com base no fator de insulina/carboidrato.
    """
    meal = Meal()

    with Database(url=os.getenv("DB_URL")) as db:
        for item in meal_input.meal:
            record = db.select(
                table_name="integrate_tables",
                id=item.food_id,
            )
            if record:
                food_item = FoodItem.from_dict(FoodItem, data=record[0])
                meal.add_item(item=food_item, grams=item.grams)
            else:
                raise HTTPException(
                    status_code=404,
                    detail=f"Food item with ID {item.food_id} not found.",
                )

    insulin_needed = None
    if meal_input.factor_insulin_cho:
        insulin_counter = InsulinCounter(meal, meal_input.factor_insulin_cho)
        insulin_needed = insulin_counter.count(meal_input.mode)

    return CalculateResponse(
        energy_kcal = meal.energy_kcal,
        carbohydrate_g = meal.carbohydrate_g,
        protein_g = meal.protein_g,
        lipid_g = meal.lipid_g,
        fiber_g = meal.fiber_g,
        insulin_needed = insulin_needed
    )


if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
