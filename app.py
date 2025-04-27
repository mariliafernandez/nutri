from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal

from src.Meal import Meal
from src.Database import Database
from src.FoodItem import FoodItem
from src.InsulinCounter import InsulinCounter
from dotenv import load_dotenv

import os


load_dotenv()
app = FastAPI()


class SearchItem(BaseModel):
    name: str | None = None
    order_by: str | None = None
    ascending: bool | None = None
    max_results: int | None = None
    categories: list[str] = []


class RelationItem(BaseModel):
    col1: str
    col2: str
    ascending: bool = False
    max_results: int | None = None
    categories: list[str] = []


class FoodPortion(BaseModel):
    food_id: int
    grams: int


class CalculateInsulinInput(BaseModel):
    meal: list[FoodPortion]
    factor_insulin_cho: int
    mode: Literal["carbo", "fpi", "fpu"] = "carbo"


class MealInput(BaseModel):
    meal: list[FoodPortion]


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


@app.get("/")
def hello_world():
    return {"Hello": "World"}


@app.get("/categories")
def get_categories():
    db = Database(os.getenv("DB_NAME"))
    db.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    categories = db.select(
        table_name="integrate_tables",
        columns="category",
        distinct=True,
    )

    return {"categories": [cat["category"] for cat in categories]}


@app.post("/search")
def search(item: SearchItem):

    db = Database(os.getenv("DB_NAME"))
    db.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    result = db.select(
        table_name="integrate_tables",
        description_like=item.name,
        categories=item.categories,
        order_by=item.order_by,
        order="ASC" if item.ascending else "DESC",
        limit=item.max_results,
    )

    return CollectionResponse(items=result)


@app.post("/relation")
def relation(item: RelationItem):

    db = Database(os.getenv("DB_NAME"))
    db.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

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


@app.post("/calculate_macros")
def calculate_macros(meal_input: MealInput):

    db = Database(os.getenv("DB_NAME"))
    db.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    meal = Meal()

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
                status_code=404, detail=f"Food item with ID {item.food_id} not found."
            )

    return meal


@app.post("/calculate_insulin")
def calculate_insulin(input_item: CalculateInsulinInput):

    db = Database(os.getenv("DB_NAME"))
    db.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    meal = Meal()

    for item in input_item.meal:
        record = db.select(
            table_name="integrate_tables",
            id=item.food_id,
        )
        if record:
            food_item = FoodItem.from_dict(FoodItem, data=record[0])
            meal.add_item(item=food_item, grams=item.grams)
        else:
            raise HTTPException(
                status_code=404, detail=f"Food item with ID {item.food_id} not found."
            )

    insulin_counter = InsulinCounter(meal, input_item.factor_insulin_cho)
    insulin_counter.count(input_item.mode)

    return {
        "items": meal.items,
        "portions": meal.portions,
        "insulin_needed": insulin_counter.count(input_item.mode),
        "mode": input_item.mode,
    }


if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
