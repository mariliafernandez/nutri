import pandas as pd
import pandas as pd
from fuzzywuzzy import process, fuzz
import json
import chromadb


client = chromadb.HttpClient()


ibge = pd.read_json("data/ibge/ibge.json")
taco = pd.read_json("data/taco/taco.json")

ibge_collection = client.get_or_create_collection(name="ibge")
taco_collection = client.get_or_create_collection(name="taco")

ibge["food_name"] = ibge["splitted"].apply(lambda x: x[0])
taco["food_name"] = taco["splitted"].apply(lambda x: x[0])

if ibge_collection.count() == 0:
    ibge_collection.add(
        documents=ibge["description"].tolist(),
        ids=[str(id) for id in ibge.index.tolist()],
        metadatas=ibge[["category", "food_name"]].to_dict(orient="records"),
    )

if taco_collection.count() == 0:
    taco_collection.add(
        documents=taco["description"].tolist(),
        ids=[str(id) for id in taco.index.tolist()],
        metadatas=taco[["category", "food_name"]].to_dict(orient="records"),
    )


def get_pd_value(row, column):
    if not row.isna()[column]:
        return float(row[column])
    else:
        return None


# Prepare the merged data
merged_data = []
taco_ids_no_match = taco["id"].to_list()
ibge_ids_no_match = ibge["id"].to_list()


# Iterate through taco descriptions and find the best match in ibge
for _, taco_row in taco.iterrows():

    merged_record = {
        "id_taco": taco_row["id"],
        "id_ibge": None,
        "description": taco_row["description"],
        "category": taco_row["category"],
        "energy_kcal": get_pd_value(taco_row, "energy_kcal"),
        "protein_g": get_pd_value(taco_row, "protein_g"),
        "lipid_g": get_pd_value(taco_row, "lipid_g"),
        "carbohydrate_g": get_pd_value(taco_row, "carbohydrate_g"),
        "fiber_g": get_pd_value(taco_row, "fiber_g"),
        "match_score": None,
        "distance": None,
        "source": "taco",
    }

    best_match = process.extractOne(
        taco_row["description"], ibge["description"], scorer=fuzz.token_sort_ratio
    )

    if best_match and best_match[1] > 86:  # Match threshold
        ibge_row = ibge[ibge["description"] == best_match[0]].iloc[0]

        ibge_id = int(ibge_row["id"])
        merged_record["id_ibge"] = ibge_id
        merged_record["match_score"] = best_match[1]

    else:
        results = ibge_collection.query(
            query_texts=[taco_row["description"]],
            where={"food_name": taco_row["food_name"]},
            n_results=1,
        )

        if len(results["documents"][0]) == 0:
            merged_data.append(merged_record)
            continue

        ibge_id = int(results["ids"][0][0])
        merged_record["id_ibge"] = ibge_id
        merged_record["distance"] = results["distances"][0][0]

    merged_data.append(merged_record)
    if ibge_id in ibge_ids_no_match:
        ibge_ids_no_match.remove(ibge_id)


# Populate the merged data with ibge records that did not match any taco records
for ibge_id in ibge_ids_no_match:
    ibge_row = ibge.iloc[ibge_id]
    merged_record = {
        "id_taco": None,
        "id_ibge": int(ibge_row["id"]),
        "description": ibge_row["description"],
        "category": ibge_row["category"],
        "energy_kcal": get_pd_value(ibge_row, "energy_kcal"),
        "protein_g": get_pd_value(ibge_row, "protein_g"),
        "lipid_g": get_pd_value(ibge_row, "lipid_g"),
        "carbohydrate_g": get_pd_value(ibge_row, "carbohydrate_g"),
        "fiber_g": get_pd_value(ibge_row, "fiber_g"),
        "match_score": None,
        "distance": None,
        "source": "ibge",
    }

    # teste.append(merged_record)
    merged_data.append(merged_record)

with open('data/categories_mapping.json', 'r', encoding='utf-8') as f:
    categories_mapping = json.load(f)

for item in merged_data:
    category = item['category'].strip()
    item['category'] = categories_mapping.get(category, item['category'])


with open("data/integrated_data.json", "w", encoding="utf-8") as f:
    json.dump(merged_data, f, ensure_ascii=False, indent=4)
