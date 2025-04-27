from src.Database import Database
import json
import os
from dotenv import load_dotenv

def load_taco():
    with open('data/taco/taco.json', 'r', encoding='utf-8') as file:
        data_taco = json.load(file)

    for item in data_taco:
        item.pop("splitted")

    try:
        db.insert("Taco", data_taco)
    except Exception as e:
        print(f"Error inserting TACO data: {e}")


def load_ibge():
    with open('data/ibge/ibge.json', 'r', encoding='utf-8') as file:
        data_ibge = json.load(file)

    for item in data_ibge:
        item.pop("splitted")

    try:
        db.insert("IBGE", data_ibge)
    except Exception as e:
        print(f"Error inserting IBGE data: {e}")


def load_integrated():
    with open('data/integrated_data.json', 'r', encoding='utf-8') as file:
        data_merged = json.load(file)

    try:
        db.insert("integrate_tables", data_merged)
    except Exception as e:
        print(f"Error inserting merged data: {e}")




if __name__ =='__main__':
    load_dotenv()

    if os.getenv("ENV") == "PROD":
        db = Database(os.getenv("DB_NAME_PROD"))
        db.connect(
            host=os.getenv("DB_HOST_PROD"),
            port=int(os.getenv("DB_PORT_PROD")),
            user=os.getenv("DB_USER_PROD"),
            password=os.getenv("DB_PASSWORD_PROD"),
        )
    else:
        db = Database(os.getenv("DB_NAME"))
        db.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )

    load_integrated()

