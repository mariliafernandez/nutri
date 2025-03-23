import json
import chromadb
from pathlib import Path

def str_to_float(s: str):
    try:
        return float(s)
    except ValueError:
        return -1


def get_key(records: list[dict], key: str, apply: callable = lambda x: x):
    return [apply(record[key]) for record in records]


def filter_records(records: list[dict], filter_keys: list, apply: list):
    return [{k: func(rec[k]) for k, func in zip(filter_keys, apply)} for rec in records]


class VectorDB:

    def __init__(self):
        self.client = chromadb.HttpClient()

    def create_collection(self, collection_name: str, json_file: Path):
        print("creating collection", collection_name)
        with open(json_file, "r", encoding="utf-8") as fp:
            taco = json.load(fp)

        documents = get_key(taco, "description")
        ids = get_key(taco, "id", str)
        metadatas = filter_records(
            records=taco,
            filter_keys=[
                "category",
                "energy_kcal",
                "protein_g",
                "lipid_g",
                "carbohydrate_g",
            ],
            apply=[str, str_to_float, str_to_float, str_to_float, str_to_float],
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

    def search(self, collection_name: str, query: str, n_results: int):
        return self.client.get_collection(collection_name).query(
            query_texts=[query], n_results=n_results
        )
