import sys
from pathlib import Path

import parcer_classes
import sqlite3_db_classes


# EXIT CODE
NO_JSON_FOUND = 1

# Ищем и создаём БД рядом с этим файлом, а не в текущей директории запуска
ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "catalog.db"

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


def main() -> None:
    finder = parcer_classes.WalkJsonFinder(root=str(ROOT))
    selection = parcer_classes.JsonSelectionByKeys({"product_name", "price", "category"})

    normalized = (
        parcer_classes.ParcerNormalizedJSONData(finder, selection, CATEGORIES_RULE).parcing()
        | parcer_classes.ParcerNormalizedJSONData(finder, selection, PRODUCTS_RULE).parcing()
    )

    with sqlite3_db_classes.CatalogDB(str(DB_PATH)) as db:
        db.save(normalized)

    print(f"Категорий: {len(normalized['categories'])}")
    print(f"Товаров: {len(normalized['products'])}")
    print(f"Сохранено в {DB_PATH.name}")


if __name__ == "__main__":
    try:
        main()
    except parcer_classes.NoJsonFiles as e:
        print(f"{e}")
        sys.exit(NO_JSON_FOUND)
