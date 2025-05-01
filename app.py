from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.Meal import Meal
from src.Database import Database
from src.FoodItem import FoodItem
from src.InsulinCounter import InsulinCounter
from src.ApiModels import (
    HealthCheckResponse,
    CategoriesResponse,
    SearchRequest,
    SearchResponse,
    RelationRequest,
    RelationResponse,
    CalculateRequest,
    CalculateResponse,
)
from dotenv import load_dotenv
import os
from fuzzywuzzy import process, fuzz

load_dotenv()

description = """
A **NutrinionALL API** facilita o acesso a informações nutricionais de alimentos e permite a integração de dados nutricionais em sua aplicação de forma simples e eficiente. Ela oferece uma solução completa para:

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

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET", "POST"])


@app.get(
    "/api/health",
    name="Health Check",
    tags=["Endpoints"],
    response_model=HealthCheckResponse,
)
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


@app.get(
    "/api/categories",
    name="Categorias Disponíveis",
    tags=["Endpoints"],
    response_model=CategoriesResponse,
)
def get_categories():
    """Retorna as categorias disponíveis no banco de dados."""
    with Database(url=os.getenv("DB_URL")) as db:
        categories = db.select(
            table_name="integrate_tables",
            columns="category",
            distinct=True,
        )

    return {"categories": [cat["category"] for cat in categories]}


@app.post(
    "/api/search",
    name="Consulta de Alimentos",
    tags=["Endpoints"],
    response_model=SearchResponse,
)
def search(item: SearchRequest):
    """
    Busca de alimentos com base nos parâmetros fornecidos. 

    Caso não seja fornecido `order_by`, a ordenação será por ID. Porém, se for fornecido `name`, o padrão da ordenação será pela similaridade com o nome do alimento. Caso `order_by` seja fornecido, a ordenação será feita por esse campo.
    """
    with Database(url=os.getenv("DB_URL")) as db:
        results = db.select(
            description_like=item.name,
            table_name="integrate_tables",
            categories=item.categories,
            order_by=item.order_by,
            order="ASC" if item.ascending else "DESC",
        )

        if len(results) == 0 and item.name:
            results = db.select(
                table_name="integrate_tables",
                categories=item.categories,
            )
            choices = [{num: r["description"]} for num, r in enumerate(results)]
            matches = process.extract(
                item.name, choices, scorer=fuzz.token_sort_ratio, limit=item.max_results
            )

            response = []
            for match in matches:
                # formato do match: ({641: 'Batata-doce, Frito(a)'}, 63)
                m, score = match
                idx, __ = m.popitem()
                if score >= 60:  # Limite de similaridade
                    response.append(results[idx])
            if item.order_by:
                response.sort(key=lambda x: x[item.order_by], reverse=not item.ascending)
            return SearchResponse(items=response)
    return SearchResponse(items=results[:item.max_results])

@app.post(
    "/api/relation",
    name="Consulta por Relações Nutricionais",
    tags=["Endpoints"],
    response_model=RelationResponse,
)
def relation(item: RelationRequest):
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
    "/api/calculate",
    name="Cálculo de Macronutrientes e Insulina",
    tags=["Endpoints"],
    response_model=CalculateResponse,
)
def calculate(meal_input: CalculateRequest):
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
        energy_kcal=meal.energy_kcal,
        carbohydrate_g=meal.carbohydrate_g,
        protein_g=meal.protein_g,
        lipid_g=meal.lipid_g,
        fiber_g=meal.fiber_g,
        percentages={
            "carbohydrate": meal.kcal_percentage("carbohydrate_g"),
            "protein": meal.kcal_percentage("protein_g"),
            "lipid": meal.kcal_percentage("lipid_g"),
        },
        insulin_needed=insulin_needed,
    )


if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
