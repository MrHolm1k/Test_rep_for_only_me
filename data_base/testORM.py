from sqlalchemy import Table, MetaData, Integer, create_engine, Column, String, Float, Boolean

# Создаём соединение
engine = create_engine("sqlite+pysqlite:///datatbase.db", echo=True)

# Metadata хранит в себе ВСЕ созданные в ней таблицы
metadate1 = MetaData()


user_table = Table(
    "students",
    metadate1,
    Column('Id', Integer, primary_key=True),
    Column('Name', String(100), nullable=False),
    Column('Group', String(20)),
    Column('GPA', Float, default=0.0),
    Column('is_acrive', Boolean)
)

# 
metadate1.create_all(engine)

metadate2 = MetaData()


user_table = Table(
    "meow",
    metadate2,
    Column('Meow', Integer, primary_key=True),
)

metadate2.create_all(engine)

