from src.VectorDB import VectorDB
from typing import Literal


class TacoCollection:

    def __init__(self):
        self.db = VectorDB()
        self.collection_name = "taco"

    def get_or_create(self, json_file="data/taco/taco.json"):
        self.collection = self.db.create_collection(self.collection_name, json_file)
        return self.collection

    def get_item(self, query):
        result = self.db.search(
            collection_name=self.collection_name, query=query, where=None, n_results=1
        )
        return FoodItem(
            **{"description": result["documents"][0]} | result["metadatas"][0]
        )

    def get_categories(self) -> list:
        metadatas = self.db.get(self.collection_name, include=["metadatas"])[
            "metadatas"
        ]
        categories = [item["category"] for item in metadatas]
        categories_list = list(set(categories))
        return categories_list

    def serialize(self, documents, metadatas):
        return [
            {"description": doc} | meta
            for doc, meta in zip(documents, metadatas)
        ]

    def get(
        self,
        where_conditions: list[dict] = [],
        order_by: (
            Literal[
                "id", "energy_kcal", "protein_g", "lipid_g", "carbohydrate_g", "fiber_g"
            ]
            | None
        ) = None,
        reverse: bool = False,
    ):
        results = self.db.get(self.collection_name, where_conditions=where_conditions)
        return self.serialize(results['documents'], results['metadatas'])

    def search(
        self,
        query: str = "",
        where_conditions: list[dict] = [],
        order_by: (
            Literal[
                "id", "energy_kcal", "protein_g", "lipid_g", "carbohydrate_g", "fiber_g"
            ]
            | None
        ) = None,
        reverse: bool = False,
        n_results: int | None = None,
    ) -> list[FoodItem]:

        results = self.db.search(
            self.collection_name,
            query=query,
            where_conditions=where_conditions,
            n_results=n_results,
        )

        results = self.serialize(results['documents'][0], results['metadatas'][0])

        if order_by is not None:
            print("order by:", order_by)
            results = sorted(
                results,
                key=lambda x: x[order_by],
                reverse=reverse,
            )

        # results_serialized = [TacoItem(**item) for item in results]

        return results
