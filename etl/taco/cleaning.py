import pandas as pd

df = pd.read_json("raw_data.json", orient="records")

df["energy_kcal"].replace("Tr", -1, inplace=True)
df["protein_g"].replace("Tr", -1, inplace=True)
df["lipid_g"].replace("Tr", -1, inplace=True)
df["carbohydrate_g"].replace("Tr", -1, inplace=True)
df["fiber_g"].replace("Tr", -1, inplace=True)

df["energy_kcal"].replace("NA", -1, inplace=True)
df["protein_g"].replace("NA", -1, inplace=True)
df["lipid_g"].replace("NA", -1, inplace=True)
df["carbohydrate_g"].replace("NA", -1, inplace=True)
df["fiber_g"].replace("NA", -1, inplace=True)

df["energy_kcal"].replace("*", -1, inplace=True)
df["protein_g"].replace("*", -1, inplace=True)
df["lipid_g"].replace("*", -1, inplace=True)
df["carbohydrate_g"].replace("*", -1, inplace=True)
df["fiber_g"].replace("*", -1, inplace=True)

df["energy_kcal"].replace("", -1, inplace=True)
df["protein_g"].replace("", -1, inplace=True)
df["lipid_g"].replace("", -1, inplace=True)
df["carbohydrate_g"].replace("", -1, inplace=True)
df["fiber_g"].replace("", -1, inplace=True)


df.loc[:, "id"] = df["id"].astype(int)
df.loc[:, "description"] = df["description"].astype(str)
df.loc[:, "category"] = df["category"].astype(str)
df.loc[:, "energy_kcal"] = df["energy_kcal"].astype(float)
df.loc[:, "protein_g"] = df["protein_g"].astype(float)
df.loc[:, "lipid_g"] = df["lipid_g"].astype(float)
df.loc[:, "carbohydrate_g"] = df["carbohydrate_g"].astype(float)
df.loc[:, "fiber_g"] = df["fiber_g"].astype(float)

df["energy_kcal"].replace(-1, None, inplace=True)
df["protein_g"].replace(-1, None, inplace=True)
df["lipid_g"].replace(-1, None, inplace=True)
df["carbohydrate_g"].replace(-1, None, inplace=True)
df["fiber_g"].replace(-1, None, inplace=True)

df["splitted"] = df["description"].apply(lambda x: [s.strip() for s in x.split(",")])

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


df[columns].to_json(
    "taco.json", orient="records", indent=4, index=False, force_ascii=False
)
