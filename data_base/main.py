import sqlite3 as sq3
import sys
from collections import defaultdict

def smart_insert(cur: sq3.Cursor, table: str, args: dict):
    
    columns = ", ".join(args.keys())
    values = tuple(args.values())
    cur.execute(f"INSERT INTO {table} ({columns})", values) 

with sq3.connect("newnewdatabse.db") as db:
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS customers(id INTEGER PRIMARY KEY, name TEXT NOT NULL);")
    cur.execute("""
                CREATE TABLE IF NOT EXISTS orders(customers_id INTEGER PRIMARY KEY, 
                amount REAL NOT NULL, id INTEGER NOT NULL, FOREIGN KEY (customers_id) REFERENCES customers(id));
                """)
    cur.execute("PRAGMA foreign_keys = ON;")

    table = input("Введи таблицу")
    args = dict()
    while True:
        choice_2 = input("1 - заполнить, 2 - выйти: ")
        match choice_2:
            case "1":
                key = input("key: ")
                choice_2 = input("1 - str, 2 - float")
 
                match choice_2:
                
                    case "1":
                        value = input("TEXT: ")
                    
                    case "2":
                        value = float(input("NUMBER"))
                    
                    case _:
                        value = None

                args[key] = value                    

            case "2":
                break

    smart_insert(cur, table, dict(args))
