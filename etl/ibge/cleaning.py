import pandas as pd
import re


def split_description(text):
    detail = None
    match = re.search(pattern=r"\(.{3,}?\)", string=text)

    if match:
        detail = match.group(0)
        text = text.replace(detail, "").strip()
        detail = detail.replace("(", "").replace(")", "").strip()

    text_splitted = [x.strip() for x in text.split(",")]
    if detail != None:
        text_splitted.append(detail)
    return text_splitted


path = r"tab01.xls"
df = pd.read_excel(path)

column_names = [
    "food_id",
    "food_description",
    "cooking_method_id",
    "cooking_method_description",
    "energy_kcal",
    "protein_g",
    "lipid_g",
    "carbohydrate_g",
    "fiber_g",
]
df.columns = column_names

categorias = df.loc[df[column_names[1:]].isnull().any(axis=1), "food_id"].to_list()
df["category"] = None
df.loc[df[column_names[1:]].isnull().any(axis=1), "category"] = categorias

df["category"] = df["category"].ffill()
df = df.dropna(subset=["food_description"])


# Replace '-' with 0 in numeric columns
df["energy_kcal"] = df["energy_kcal"].replace("-", 0)
df["protein_g"] = df["protein_g"].replace("-", 0)
df["lipid_g"] = df["lipid_g"].replace("-", 0)
df["carbohydrate_g"] = df["carbohydrate_g"].replace("-", 0)
df["fiber_g"] = df["fiber_g"].replace("-", 0)

# Convert columns to appropriate data types
df.loc[:, "food_id"] = df["food_id"].astype(str)
df.loc[:, "food_description"] = df["food_description"].astype(str)
df.loc[:, "cooking_method_id"] = df["cooking_method_id"].astype(int)
df.loc[:, "cooking_method_description"] = df["cooking_method_description"].astype(str)
df.loc[:, "energy_kcal"] = df["energy_kcal"].astype(float)
df.loc[:, "protein_g"] = df["protein_g"].astype(float)
df.loc[:, "lipid_g"] = df["lipid_g"].astype(float)
df.loc[:, "carbohydrate_g"] = df["carbohydrate_g"].astype(float)
df.loc[:, "fiber_g"] = df["fiber_g"].astype(float)
df.loc[:, "category"] = df["category"].astype(str)

df["description"] = None
df.loc[:, "description"] = (
    df["food_description"] + ", " + df["cooking_method_description"]
)
df.loc[:, "description"] = df["description"].replace(", Não se aplica", "")

df.loc[:, "description"] = df["description"].replace(", Não se aplica", "", regex=True)
df.reset_index(inplace=True)
df["id"] = df.index.to_list()

df["splitted"] = df["description"].apply(split_description)

columns = [
    "id",
    "description",
    "category",
    "splitted",
    "energy_kcal",
    "protein_g",
    "lipid_g",
    "carbohydrate_g",
    "fiber_g",
]

df[columns].to_json("ibge.json", orient="records", indent=4, force_ascii=False)
