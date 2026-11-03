import sqlite3


SCHEMA = """
CREATE TABLE IF NOT EXISTS categories (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE IF NOT EXISTS products (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    price        REAL NOT NULL,
    category_id  INTEGER NOT NULL REFERENCES categories(id)
);
"""


class CatalogDB:
    def __init__(self, path: str = "catalog.db"):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.executescript(SCHEMA)

    def __enter__(self) -> "CatalogDB":
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.conn.close()

    def save(self, normalized: dict[str, list[dict]]) -> None:
        
# Повторный запуск не должен плодить дубли,
# поэтому чистим в порядке, безопасном для внешнего ключа
        
        self.conn.execute("DELETE FROM products")
        self.conn.execute("DELETE FROM categories")

        category_ids = self._insert_categories(normalized["categories"])
        self._insert_products(normalized["products"], category_ids)

    def _insert_categories(self, rows: list[dict]) -> dict[str, int]:
        ids = dict()

        for row in rows:
            cursor = self.conn.execute(
                "INSERT INTO categories(name, description) VALUES (?, ?)",
                (row["name"], row["description"]),
            )
            ids[row["name"]] = cursor.lastrowid

        return ids

    def _insert_products(self, rows: list[dict], category_ids: dict[str, int]) -> None:
        self.conn.executemany(
            "INSERT INTO products(product_name, price, category_id) VALUES (?, ?, ?)",
            [
                (row["product_name"], row["price"], category_ids[row["category_name"]])
                for row in rows
            ],
        )
