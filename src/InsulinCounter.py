from typing import Literal

class InsulinCounter:
    def __init__(self, meal, factor_insulin_cho):
        self.meal = meal
        self.factor_insulin_cho = factor_insulin_cho

    def count(self, mode:Literal["carbo", "fpi", "fpu"] = "carbo"):
        """Calculate the insulin needed for the meal considering the mode"""
        if mode == "carbo":
            return self.count_carbo()
        elif mode == "fpi":
            return self.fat_protein_increment()
        elif mode == "fpu":
            return self.fat_protein_unit()
        else:
            raise ValueError("Invalid mode. Choose 'carbo', 'fpi', or 'fpu'.")

    def count_carbo(self):
        """Calculate the insulin needed for the meal considering only carbohydrates"""
        total_cho = sum(
            item.carbohydrate_g * portion
            for item, portion in zip(self.meal.items, self.meal.portions)
        )
        insulin_needed = total_cho / self.factor_insulin_cho
        return insulin_needed

    def fat_protein_increment(self, factor: float = 0.3):
        """Calculate the insulin needed for the meal considering fat and proteins by an increment factor"""
        return self.count_carbo() * (1 + factor)

    def fat_protein_unit(self):
        """Calculate the insulin needed for the meal using Fat-Protein Units"""
        calories_protein_lipid = self.meal.protein_g * 4 + self.meal.lipid_g * 9
        carbo_g = calories_protein_lipid / 10
        return self.count_carbo() + carbo_g / self.factor_insulin_cho


# # id, id_taco, id_ibge, distance, match_score, description, category, energy_kcal, protein_g, lipid_g, carbohydrate_g, fiber_g, source
# '2397', '416', '1813', '0.587584', NULL, 'Hambúrguer, bovino, frito', 'Carnes e derivados', '258.283', '19.9729', '17.0123', '6.32008', NULL, 'taco'
