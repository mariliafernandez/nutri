from pydantic import BaseModel
from typing import Literal
from pydantic_settings import SettingsConfigDict
import json
from pathlib import Path


def load_json_schema(file_name: str) -> dict:
    schemas_path = Path("json_schemas/")
    with open(schemas_path / file_name, "r", encoding="utf-8") as file:
        return json.load(file)


class HealthCheckResponse(BaseModel):
    status: Literal["ok", "nok"]
    db_error: str | None = None
    model_config = SettingsConfigDict(
        json_schema_extra=load_json_schema("HealthCheckResponse.json"),
    )


class CategoriesResponse(BaseModel):
    categories: list[str]
    model_config = SettingsConfigDict(
        json_schema_extra=load_json_schema("CategoriesResponse.json"),
    )


class SearchRequest(BaseModel):
    name: str | None = None
    order_by: Literal[
        "energy_kcal", "protein_g", "lipid_g", "carbohydrate_g", "fiber_g"
    ] = None
    ascending: bool = False
    max_results: int | None = None
    categories: list[str] = []
    model_config = SettingsConfigDict(
        populate_by_name=True,
        json_schema_extra=load_json_schema("SearchRequest.json"),
    )


class SearchItemResponse(BaseModel):
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
    model_config = SettingsConfigDict(
        json_schema_extra=load_json_schema("SearchItemResponse.json"),
    )


class SearchResponse(BaseModel):
    items: list[SearchItemResponse]


class RelationRequest(BaseModel):
    col1: Literal["energy_kcal", "protein_g", "lipid_g", "carbohydrate_g", "fiber_g"]
    col2: Literal["energy_kcal", "protein_g", "lipid_g", "carbohydrate_g", "fiber_g"]
    ascending: bool = False
    max_results: int | None = None
    categories: list[str] = []
    model_config = SettingsConfigDict(
        populate_by_name=True,
        json_schema_extra=load_json_schema("RelationRequest.json"),
    )


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
    model_config = SettingsConfigDict(
        json_schema_extra=load_json_schema("RelationItemResponse.json"),
    )


class RelationResponse(BaseModel):
    items: list[RelationItemResponse]


class FoodPortion(BaseModel):
    food_id: int
    grams: int
    model_config = SettingsConfigDict(
        json_schema_extra=load_json_schema("FoodPortion.json"),
    )


class CalculateRequest(BaseModel):
    meal: list[FoodPortion]
    factor_insulin_cho: int = None
    mode: Literal["carbo", "fpi", "fpu"] = "carbo"
    model_config = SettingsConfigDict(
        populate_by_name=True,
        json_schema_extra=load_json_schema("CalculateRequest.json"),
    )


class CalculateResponse(BaseModel):
    energy_kcal: float
    carbohydrate_g: float
    protein_g: float
    lipid_g: float
    fiber_g: float
    insulin_needed: float | None
    model_config = SettingsConfigDict(
        json_schema_extra=load_json_schema("CalculateResponse.json"),
    )
