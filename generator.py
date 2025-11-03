import psycopg as ps
from os import getenv
from dotenv import load_dotenv
from faker import Faker
from random import randint, choice

load_dotenv()
fake = Faker("pl_PL")

DB_NAME = getenv("DB_NAME")
SQL_USER = getenv("SQL_USER")
SQL_PASSWORD = getenv("SQL_PASSWORD")
DB_HOST = getenv("DB_HOST")

with ps.connect(f"dbname={DB_NAME} user={SQL_USER} password={SQL_PASSWORD} host={DB_HOST}") as conn:
    with conn.cursor() as cur:

        cur.execute("TRUNCATE TABLE szczegolyzam, zamowienia, produkt, producent, klient, kategoria RESTART IDENTITY CASCADE;")

        with open("testowe_dane.sql", "r", encoding="UTF-8") as file:
            sql = file.read()
            cur.execute(sql)

        client_ids = []
        for _ in range(5):
            client_name = fake.first_name()
            client_surname = fake.last_name()
            is18 = False
            if randint(0,99) >= 18:
                is18 = True
            login = client_name + "." + client_surname + ".mch"
            password = fake.password()
            mail = fake.email()
            telephone = fake.phone_number()[:15]
            cur.execute("INSERT INTO klient (imie, nazwisko, czy_18plus, login, haslo, email, telefon) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id_klienta", (client_name, client_surname, is18, login, password, mail, telephone))
            client_ids.append(cur.fetchone()[0])

        orders_ids = []
        STATUS = ["OCZEKUJĄCE", "WYSŁANE", "DOSTARCZONE"]

        for _ in range(5):
            client_id = choice(client_ids)
            date = fake.date_between(start_date="-1w")
            status = choice(STATUS)
            cost = 0.0
            cur.execute("INSERT INTO zamowienia (id_klienta, data, status, kwota) VALUES (%s, %s, %s, %s) RETURNING id_zam", (client_id, date, status, cost))
            orders_ids.append(cur.fetchone()[0])

        products_list = []

        products = cur.execute("SELECT * FROM produkt;")

        for i in products:
            products_list.append(i[0])

        used = set()
        counter = 0
        for _ in range(6):
            order_id = choice(orders_ids)
            if counter < 5:
                while order_id in used:
                    order_id = choice(orders_ids)
            counter += 1
            used.add(order_id)
            id_prod = choice(products_list)
            count = randint(1,10)
            cur.execute("SELECT cena FROM produkt WHERE id_prod = 1;")
            this_cost = cur.fetchone()[0]
            this_cost *= count
            cur.execute("INSERT INTO szczegolyzam (id_zam, id_prod, ilosc, cena) VALUEs (%s, %s, %s, %s)", (order_id, id_prod, count, this_cost))


        cur.execute("SELECT * FROM szczegolyzam;")

        x = cur.fetchall()
        cos = {}
        for i in range(len(x)):
            if x[i][1] not in cos:
                cos[x[i][1]] = x[i][4]
            else:
                cos[x[i][1]] += x[i][4]

        print(cos)

        for k, v in cos.items():
            cur.execute(f"UPDATE zamowienia SET kwota = {float(v)} WHERE id_zam = {k}")



