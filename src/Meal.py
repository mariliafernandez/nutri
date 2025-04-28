from src.FoodItem import FoodItem

from typing import Literal


class Meal:
    def __init__(
        self,
        type: Literal[
            "café da manhã",
            "lanche da manhã",
            "almoço",
            "lanche da tarde",
            "jantar",
            "ceia",
        ] = None,
    ):
        self.items = []
        self.portions = []
        self.carbohydrate_g = 0
        self.protein_g = 0
        self.lipid_g = 0
        self.energy_kcal = 0
        self.fiber_g = 0
        self.type = type

    def __repr__(self):
        string = f"Refeição: {self.type}\n-----"
        for i in range(len(self.items)):
            string += f"\n{str(self.items[i].description)}, {self.portions[i] * self.items[i].grams} g"
        string += f"\n-----\ncarboidratos: {round(self.carbohydrate_g, 2)}\nproteínas: {round(self.protein_g, 2)}\ngorduras: {round(self.lipid_g, 2)}\ncalorias: {round(self.energy_kcal, 2)}\n-----"
        return string

    def add(self, attr: str, item: FoodItem, portion: float):
        if item.__getattribute__(attr) is not None:
            sum = self.__getattribute__(attr) + item.__getattribute__(attr) * portion
            self.__setattr__(attr, sum)

    def remove(self, attr: str, item: FoodItem, portion: float):
        if item.__getattribute__(attr) is not None:
            sum = self.__getattribute__(attr) - item.__getattribute__(attr) * portion
            self.__setattr__(attr, sum)

    def add_item(self, item: FoodItem, portion: float = None, grams: float = None):
        if portion is None and grams is not None:
            portion = grams / item.grams
        self.items.append(item)
        self.portions.append(portion)

        self.add("carbohydrate_g", item, portion)
        self.add("protein_g", item, portion)
        self.add("lipid_g", item, portion)
        self.add("fiber_g", item, portion)
        self.add("energy_kcal", item, portion)

    def remove_item(self, index: int):
        item = self.items[index]
        portion = self.portions[index]

        self.remove("carbohydrate_g", item, portion)
        self.remove("protein_g", item, portion)
        self.remove("lipid_g", item, portion)
        self.remove("fiber_g", item, portion)
        self.remove("energy_kcal", item, portion)

        del self.items[index]
        del self.portions[index]
