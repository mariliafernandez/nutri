from src.VectorDB import VectorDB


class TacoItem:

    def __init__(
        self,
        description: str,
        category: str,
        energy_kcal: float,
        protein_g: float,
        lipid_g: float,
        carbohydrate_g: float,
        grams:int = 100
    ):
        self.description = description
        self.category = category
        self.energy_kcal = energy_kcal
        self.protein_g = protein_g
        self.lipid_g = lipid_g
        self.carbohydrate_g = carbohydrate_g
        self.grams = grams

    def __str__(self):
        return f"{self.description}, {self.grams}g [{self.category}]:\ncarboidratos: {round(self.carbohydrate_g, 2)} g\nproteínas: {round(self.protein_g, 2)}g\ngorduras: {round(self.lipid_g, 2)} g\ncalorias:{round(self.energy_kcal, 2)}kcal"

    def fraction(self, grams: float):
        return TacoItem(
            self.description,
            self.category,
            self.energy_kcal * grams / 100,
            self.protein_g * grams / 100,
            self.lipid_g * grams / 100,
            self.carbohydrate_g * grams / 100,
            grams
        )


class TacoCollection:

    def __init__(self, collection_name: str = "taco"):
        self.db = VectorDB()
        self.collection_name = collection_name

    def get_or_create(self, json_file):
        return self.db.create_collection(self.collection_name, json_file)

    def search(self, query: str, n_results: int):
        results = self.db.search(self.collection_name, query, n_results)
        self.taco_items = [
            TacoItem(**{"description": doc} | meta)
            for doc, meta in zip(results["documents"][0], results["metadatas"][0])
        ]
        return self.taco_items

    def __str__(self):
        return [str(item) for item in self.taco_items]
