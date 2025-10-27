import psycopg as pies
from dotenv import load_dotenv
from os import getenv

load_dotenv()   # loads enviromental variables

DB_NAME = getenv("DB_NAME")
SQL_USER = getenv("SQL_USER")
SQL_PASSWORD = getenv("SQL_PASSWORD")

with pies.connect(f"dbname={DB_NAME} user={SQL_USER} password={SQL_PASSWORD}") as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM transport;")
        for record in cur:
            print(record)