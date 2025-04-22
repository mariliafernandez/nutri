# https://www.nepa.unicamp.br/wp-content/uploads/sites/27/2023/10/Taco-4a-Edicao.xlsx

from src.Meal import Meal
from src.constants import CATEGORIES, GROUPS
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from src.Database import Database

# from flask import Flask, request, render_template
from typing import Literal
import re
import json

app = FastAPI()


class SearchItem(BaseModel):
    name: str | None = None
    order_by: str | None = None
    ascending: bool | None = None
    categories: list[str] = []
    max_results: int = 5


@app.post("/search")
def search(item: SearchItem):
    db = Database("nutrition")
    db.connect()
    
    result = db.select(
        table_name="integrate_tables",
        description_like=item.name,  
        order_by=item.order_by,
        order="ASC" if item.ascending else "DESC", 
    )
    return result


# @app.route("/", methods=["GET", "POST"])
# def home():
#     print("request:")
#     taco = TacoCollection()
#     taco.get_or_create()
#     categories = [c | {"selected":True} for c in CATEGORIES]

#     if request.method == "POST":
#         data = request.form
#         query = data.get("query", "")
#         categories = data.get("categories", categories)
#         selected_order_by = data.get("order_by", None)
#         order = data.get("order", "ascending")
#         taco_items = taco.search(
#             query=query,
#             order_by=selected_order_by,
#             reverse = order == "descending",
#             where_conditions=[
#                 {"category": get_category_name_by_id(category_id)}
#                 for category_id in categories
#             ],
#         )
#     else:
#         taco_items = taco.get()
#         selected_order_by = None
#         query = ""

#     data = {
#         "categories": categories,
#         "order_by": GROUPS,
#         "selected_order_by": selected_order_by,
#         "query": query,
#         "taco_items": taco_items,
#     }
#     return render_template("index.html", data=data)


def split_values(string):
    pattern = r"[1-9][0-9]*\s?g"
    value = re.search(pattern, string)
    if value:
        grams_str = value.group()
        grams_int = int(grams_str.replace("g", ""))
        food = string.replace(grams_str, "")
        return (food, grams_int)
    return (string, 100)


def get_category_name_by_id(id):
    for item in CATEGORIES:
        if item["id"] == int(id):
            return item["category"]
