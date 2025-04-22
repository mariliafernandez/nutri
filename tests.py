from src.FoodItem import FoodItem
from src.Meal import Meal
from src.InsulinCounter import InsulinCounter
from src.Database import Database, QueryFactory


def test_insulin_count():
    item = FoodItem(
        id=1,
        description="Hambúrguer, bovino, grelhado",
        category="Carnes e derivados",
        energy_kcal=209.8316666667,
        protein_g=13.15625,
        lipid_g=12.4303333333,
        carbohydrate_g=11.3334166667,
        fiber_g=None,
    )
    meal= Meal(type="lanche")
    meal.add_item(item, 1.8)
    counter = InsulinCounter(meal, 10)
    
    print(meal)
    print("count_carbo", counter.count_carbo())
    print("fat_protein_increment", counter.fat_protein_increment())
    print("fpu", counter.fpu())


def test_make_query():

    query_factory = QueryFactory(
        table_name="table_integrated", 
        columns="*", 
        where_conditions=[{"description":"hamburguer"}],
        order_by="energy_kcal",
        order="DESC",
        )
    query_factory.make_select()

    print(query_factory.query)


def test_select_like():
    db = Database("nutrition")
    db.connect()
    result = db.select(
        table_name="integrate_tables",
        columns="id",
        description_like="hamburguer",
        order_by="energy_kcal",
        order="DESC",
    )
    for r in result:
        print(r)
    
def test_select_by_id():
    db = Database("nutrition")
    db.connect()
    result = db.select(
        table_name="integrate_tables",
        id=4086
    )
    for r in result:
        print(r)
    
if __name__ == "__main__":

    test_select_by_id()
