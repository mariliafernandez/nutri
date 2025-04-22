import json
import chromadb
from pathlib import Path
from typing import Literal


def str_to_float(s: str):
    try:
        return float(s)
    except ValueError:
        return -1


def get_key(records: list[dict], key: str, apply: callable = lambda x: x):
    return [apply(record[key]) for record in records]


def filter_records(records: list[dict], filter_keys: list, apply: list):
    if len(filter_keys) != len(apply):
        raise Exception("filter_keys and apply lists must have equal sizes")

    return [{k: func(rec[k]) for k, func in zip(filter_keys, apply)} for rec in records]


class VectorDB:

    def __init__(self):
        self.client = chromadb.HttpClient()

    def create_collection(self, collection_name: str, json_file: Path):
        print("consulting/creating collection", collection_name)
        with open(json_file, "r", encoding="utf-8") as fp:
            taco = json.load(fp)

        documents = get_key(taco, "description")
        ids = get_key(taco, "id", str)
        metadatas = filter_records(
            records=taco,
            filter_keys=[
                "id",
                "category",
                "energy_kcal",
                "protein_g",
                "lipid_g",
                "fiber_g",
                "carbohydrate_g",
            ],
            apply=[
                int,
                str,
                str_to_float,
                str_to_float,
                str_to_float,
                str_to_float,
                str_to_float,
            ],
        )

        collection = self.client.get_or_create_collection(collection_name)

        if collection.count() < len(taco):
            print("adding documents to collection")
            collection.add(
                documents=documents,  # we embed for you, or bring your own
                metadatas=metadatas,  # filter on arbitrary metadata!
                ids=ids,  # must be unique for each doc
            )

        return collection

    def count(self, collection_name: str) -> int:
        return self.client.get_collection(collection_name).count()

    def search(
        self,
        collection_name: str,
        query: str = "",
        where_conditions: list[dict] = [],
        n_results: int | None = None,
    ):
        # https://cookbook.chromadb.dev/core/filters/
        if n_results == None:
            n_results = self.count(collection_name)

        where_conditions = self.build_where(where_conditions, operator="or")

        return self.client.get_collection(collection_name).query(
            query_texts=[query], where=where_conditions, n_results=n_results
        )

    def build_where(self, where_conditions: list, operator: Literal["or", "and"]):
        # where={"$and": [{"metadata_field1": "value1"}, {"metadata_field2": "value2"}]}
        if len(where_conditions) > 1:
            print("where:", {f"${operator}": where_conditions})
            return {f"${operator}": where_conditions}
        if len(where_conditions) == 1:
            print("where:", where_conditions[0])
            return where_conditions[0]
        return None

    def get(
        self,
        collection_name: str,
        where_conditions: list[dict] = [],
        include: list = ["metadatas", "documents"],
    ):
        where = self.build_where(where_conditions, operator="or")
        return self.client.get_collection(collection_name).get(
            where=where, include=include
        )
