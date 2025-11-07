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
            AND = False

            print("Welcome in our shop!")

            while not logout:

                print_from_db(cur, default_query(), True)

                print("What would u like to do? [1 - Filter, 2 - Clear filters, 3 - exit]")

                x = int(input("> "))

                if x == 1:
                    PACAGE = filters(QUERY, cur, AND)
                    QUERY, AND = PACAGE
                if x == 2:
                    QUERY = default_query()
                    AND = False
                if x == 3:
                    logout = True
                    conn.close() # -> for now, in future it will come back to logging page

                #print(QUERY)

def default_query():
    return "SELECT produkt.* FROM produkt JOIN kategoria ON produkt.id_kat = kategoria.id_kat JOIN producent ON produkt.id_firmy = producent.id_firmy WHERE (produkt.stan_wirtualny IS NOT NULL AND produkt.stan_wirtualny > 0)"

def print_from_db(cur, QUERY, mainQUERY):
    if mainQUERY == True:
        for record in cur.execute(QUERY + "ORDER BY id_prod;"):
            cost = f"{record[3]:>7.2f} zł"
            print(f'{record[0]:<3} | {record[1]:^25} | {record[2]:^55} | {cost:^12} | {record[5]:>3} {record[8]}\n')
    else:
        for record in cur.execute(QUERY + ";"):
            print(record[0])

def filters(QUERY, cur, AND):
    print("Choose your filter!")
    print("1 - Nazwa, 2 - Kategoria, 3 - Producent, 4 - Cena")

    QUERY_HOLDER = ""

    wybor = int(input("> "))
    print("\n")

    if wybor == 1:
        nazwa = input("Input name!\n> ")
        QUERY_HOLDER = f" produkt.nazwa LIKE '%{nazwa}%'"

    elif wybor == 2:
        print("Avaiable categories:")
        print_from_db(cur, "SELECT nazwa FROM kategoria;", False)

        category = input("Choose category!\n> ")
        QUERY_HOLDER = f" kategoria.nazwa = '{category}'"

    elif wybor == 3:
        print("Avaiable producents:")
        print_from_db(cur, "SELECT nazwa FROM producent;", False)

        producent = input("Choose producer!\n> ")
        QUERY_HOLDER = f" producent.nazwa = '{producent}'"

    elif wybor == 4:
        print("Specify price:")
        x, y = map(float, input("Give two numbers: 10 100\n>").split())
        QUERY_HOLDER = f" produkt.cena BETWEEN {x} AND {y}"

    QUERY += (" AND" + QUERY_HOLDER)

    print("\n")
    return QUERY, AND

def koszyk():
    pass


if __name__ == "__main__":
    main_loop()