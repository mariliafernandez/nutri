# https://www.nepa.unicamp.br/wp-content/uploads/sites/27/2023/10/Taco-4a-Edicao.xlsx

from src.Taco import TacoCollection
import re

def split_values(string):
    pattern = r"[1-9][0-9]*\s?g"
    value = re.search(pattern, string)
    if value:
        grams_str = value.group()
        grams_int = int(grams_str.replace("g", ""))
        food = string.replace(grams_str, "")
        return (food, grams_int)
    return (string, 100)


if __name__ == "__main__":
    collection = TacoCollection(collection_name="taco")
    collection.get_or_create("data/taco.json")
    query = input("Entre com a busca (ou 0 para sair): ")

    while query != "0":
        food, qt_grams = split_values(query)
        results = collection.search(food, 3)
        for result in results:
            print(result.fraction(qt_grams))
        query = input("\nEntre com a busca (ou 0 para sair): ")
        
