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
        self.type = type


    def __repr__(self):
        string = f"Refeição: {self.type}\n-----"
        for i in range(len(self.items)):
            string += f"\n{str(self.items[i].description)}, {self.portions[i] * self.items[i].grams} g"
        string += f"\n-----\ncarboidratos: {round(self.carbohydrate_g, 2)}\nproteínas: {round(self.protein_g, 2)}\ngorduras: {round(self.lipid_g, 2)}\ncalorias: {round(self.energy_kcal, 2)}\n-----"
        return string

    def add_item(self, item: FoodItem, portion: float = None, grams: float = None):
        if portion is None and grams is not None:
            portion = grams / item.grams
        self.items.append(item)
        self.portions.append(portion)
        self.carbohydrate_g += item.carbohydrate_g * portion
        self.protein_g += item.protein_g * portion
        self.lipid_g += item.lipid_g * portion
        self.energy_kcal += item.energy_kcal * portion

    def remove_item(self, index: int):
        item = self.items[index]
        portion = self.portions[index]
        self.carbohydrate_g -= item.carbohydrate_g * portion
        self.protein_g -= item.protein_g * portion
        self.lipid_g -= item.lipid_g * portion
        self.energy_kcal -= item.energy_kcal * portion
        del self.items[index]
        del self.portions[index]

