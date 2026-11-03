import sys
from pathlib import Path
from sqlalchemy import Table, MetaData, Integer, create_engine, Column, String, Float, Boolean, Engine, ForeignKey, Connection, insert


import parcer_classes

# TODO: Написать UI для более удобного использования данного скрипта


# EXIT CODES
NO_JSON_FOUND = 1

# Ищем и создаём БД рядом с этим файлом, а не в текущей директории запуска
ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "sql_alchemy_catalog.db"

CATEGORIES_RULE = parcer_classes.TableRule(
    table="categories",
    entity_path=("category",),
    key_path=("name",),
    fields={"name": ("name",), "description": ("description",)},
)

PRODUCTS_RULE = parcer_classes.TableRule(
    table="products",
    entity_path=(),
    key_path=("product_name",),
    fields={
        "product_name": ("product_name",),
        "price": ("price",),
        "category_name": ("category", "name"),
    },
    deduplicate=False,
)

def create_table(engine: Engine) -> dict[str, Table]:
    
    metadata = MetaData()

    categories = Table(
        "categories",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("name", String, nullable=False, unique=True),
        Column("description", String, nullable=True)
    )
    
    products = Table(
        "products",
        metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("product_name", String, nullable=False),
        Column("price", Float, nullable=False),
        Column("category_id", Integer, ForeignKey("categories.id"), nullable=False)
    )
    
    metadata.create_all(engine)

    metadict = {"categories": categories, "products": products}

    return metadict

def insert_into_catagories(connection: Connection, metatabel: Table,  rows: list[dict]) -> dict[str, int]:
    
    ids = dict()

    for row in rows:
        statment = insert(metatabel).values(name=row["name"], description=row["description"])
        result = connection.execute(statment)
        ids[row["name"]] = result.inserted_primary_key[0]

    return ids

def insert_into_productes(connection: Connection, metatabel: Table,  rows: list[dict], ids: dict[str, int]) -> None:
    for row in rows:
        statment = insert(metatabel).values(category_id=ids[row["category_name"]], product_name=row["product_name"], price=row["price"])
        connection.execute(statment)

        
    

def main():
    finder = parcer_classes.WalkJsonFinder(root=str(ROOT))
    selection = parcer_classes.JsonSelectionByKeys({"product_name", "price", "category"})

    normalized = (
        parcer_classes.ParcerNormalizedJSONData(finder, selection, CATEGORIES_RULE).parcing()
        | parcer_classes.ParcerNormalizedJSONData(finder, selection, PRODUCTS_RULE).parcing()
    )
    
    engine = create_engine(f"sqlite+pysqlite:///{str(DB_PATH)}")
    
    meta_dict = create_table(engine)
       
    with engine.connect() as connection:
        
        ids = insert_into_catagories(connection, meta_dict["categories"], normalized["categories"])
        
        insert_into_productes(connection, meta_dict["products"], normalized["products"], ids)
        connection.commit()


if __name__ == "__main__":
    try:
        main()
    except parcer_classes.NoJsonFiles as e:
        print(f"{e}")
        sys.exit(NO_JSON_FOUND)
