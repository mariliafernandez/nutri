

class FoodItem:

    def __init__(
        self,
        id: int,
        description: str,
        category: str,
        energy_kcal: float,
        protein_g: float,
        lipid_g: float,
        carbohydrate_g: float,
        fiber_g: float,
        source: str,
        grams: int = 100,
    ):
        self.id = id
        self.description = description
        self.category = category
        self.energy_kcal = energy_kcal
        self.protein_g = protein_g
        self.lipid_g = lipid_g
        self.carbohydrate_g = carbohydrate_g
        self.fiber_g = fiber_g
        self.grams = grams
        self.source = source

    def from_dict(cls, data: dict):
        """Create a FoodItem instance from a dictionary."""
        return cls(
            id=data.get("id"),
            description=data.get("description"),
            category=data.get("category"),
            source=data.get("source"),
            energy_kcal=data.get("energy_kcal", None),
            protein_g=data.get("protein_g", None),
            lipid_g=data.get("lipid_g", None),
            carbohydrate_g=data.get("carbohydrate_g", None),
            fiber_g=data.get("fiber_g", None),
        )

    def __str__(self):
        return f"{self.description}, {self.grams}g [{self.category}]:\ncarboidratos: {round(self.carbohydrate_g, 2)} g\nproteínas: {round(self.protein_g, 2)}g\ngorduras: {round(self.lipid_g, 2)} g\nfibras: {round(self.fiber_g, 2)}g\ncalorias: {round(self.energy_kcal, 2)}kcal"

    def __repr__(self):
        return self.__str__()

    def fraction(self, grams: float):
        return FoodItem(
            self.description,
            self.category,
            self.energy_kcal * grams / 100,
            self.protein_g * grams / 100,
            self.lipid_g * grams / 100,
            self.fiber_g * grams / 100,
            self.carbohydrate_g * grams / 100,
            grams,
        )
