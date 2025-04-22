from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Food(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    description: str = Field(index=True)
    energy_kcal: float
    protein_g: float
    lipid_g: float
    carbohydrate_g: float
    fiber_g: float
    grams: int = 100,
    taco: "TacoTable" | None = Field(default=None, foreign_key="taco.id")
    ibge: "IBGETable" | None = Field(default=None, foreign_key="ibge.id")



class TacoTable(SQLModel, table=True):
    pass

class IBGETable(SQLModel, table=True):
    pass

