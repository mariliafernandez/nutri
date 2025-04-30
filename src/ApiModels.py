from pydantic import BaseModel, Field, field_serializer
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
    name: str = Field(default=None, description="Nome do alimento a ser pesquisado")
    order_by: Literal[
        "energy_kcal", "protein_g", "lipid_g", "carbohydrate_g", "fiber_g"
    ] = Field(
        default=None, description="Ordenação customizada, apenas se `name=null`")
    
    ascending: bool = Field(
        default=False,
        description="Ordenar os resultados em ordem crescente",
    )
    max_results: int = Field(
        default=None,
        description="Número máximo de resultados a serem retornados (por padrão retorna todos)",
    )
    categories: list[str] = Field(
        default=[],
        description="Filtro de categorias (por padrão busca em todas as categorias)",
    )
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


class EnergyPercentages(BaseModel):
    carbohydrate: float
    protein: float
    lipid: float

    @field_serializer("carbohydrate", "protein", "lipid")
    def round_float(self, value: float) -> float:
        return round(value)


class CalculateResponse(BaseModel):
    energy_kcal: float
    carbohydrate_g: float
    protein_g: float
    lipid_g: float
    fiber_g: float
    percentages: EnergyPercentages
    insulin_needed: float | None = Field(
        default=None, description="Insulina necessária em UI"
    )
    model_config = SettingsConfigDict(
        json_schema_extra=load_json_schema("CalculateResponse.json"),
    )

    @field_serializer(
        "energy_kcal",
        "carbohydrate_g",
        "protein_g",
        "lipid_g",
        "fiber_g",
        "insulin_needed",
    )
    def round_float(self, value: float) -> float:
        return round(value, 2) if value is not None else None
