import psycopg as ps
from dotenv import load_dotenv
from os import getenv

load_dotenv()   # loads enviromental variables

DB_NAME = getenv("DB_NAME")
SQL_USER = getenv("SQL_USER")
SQL_PASSWORD = getenv("SQL_PASSWORD")
DB_HOST = getenv("DB_HOST")

def main_loop():
    with ps.connect(f"dbname={DB_NAME} user={SQL_USER} password={SQL_PASSWORD} host={DB_HOST}") as conn:
        with conn.cursor() as cur:
            logout = False
            while not logout:
                print("What do u want? [1 - Show products, 2 - exit]")
                x = int(input("> "))
                if x == 1:
                    for record in cur.execute("SELECT * FROM produkt;"):
                        cost = f"{record[3]:>7.2f} zł"
                        print(f'{record[0]:<3} | {record[1]:^25} | {record[2]:^55} | {cost:^12} | {record[5]:>3} {record[8]}\n')
                if x == 2:
                    logout = True
                    conn.close()

def filters():
    pass

def koszyk():
    pass

    

if __name__ == "__main__":
    main_loop()