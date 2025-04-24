from fastapi import FastAPI
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
db = Database("nutrition")
db.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)


class SearchItem(BaseModel):
    name: str | None = None
    order_by: str | None = None
    ascending: bool | None = None
    max_results: int | None = None
    categories: list[str] = []


class FoodPortion(BaseModel):
    food_id: int
    grams: int


class MealInput(BaseModel):
    items: list[FoodPortion] = []


class CalculateInsulinInput(BaseModel):
    meal: MealInput
    factor_insulin_cho: int
    mode: Literal["carbo", "fpi", "fpu"] = "carbo"


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/search")
def search(item: SearchItem):
    result = db.select(
        table_name="integrate_tables",
        description_like=item.name,
        categories=item.categories,
        order_by=item.order_by,
        order="ASC" if item.ascending else "DESC",
        limit=item.max_results,
    )
    return result


@app.post("/calculate_macros")
def calculate_macros(meal_input: MealInput):
    meal = Meal()

    for item in meal_input.items:
        records = db.select(
            table_name="integrate_tables",
            id=item.food_id,
        )
        if records:
            food_item = FoodItem.from_dict(FoodItem, data=records[0])
            meal.add_item(item=food_item, grams=item.grams)

        # TODO: Add error handling for food items not found in the database

    return meal


@app.post("/calculate_insulin")
def calculate_insulin(input_item: CalculateInsulinInput):
    meal = Meal()

    for item in input_item.meal.items:
        records = db.select(
            table_name="integrate_tables",
            id=item.food_id,
        )
        if records:
            food_item = FoodItem.from_dict(FoodItem, data=records[0])
            meal.add_item(item=food_item, grams=item.grams)

        # TODO: Add error handling for food items not found in the database

    insulin_counter = InsulinCounter(meal, input_item.factor_insulin_cho)
    insulin_counter.count(input_item.mode)

    return {
        "meal": meal,
        "insulin_needed": insulin_counter.count(input_item.mode),
        "mode": input_item.mode,
    }
