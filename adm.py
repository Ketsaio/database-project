import psycopg
from dotenv import load_dotenv
from os import getenv

load_dotenv()   # loads enviromental variables

DB_NAME = getenv("DB_NAME")
DB_HOST = getenv("DB_HOST")
SQL_USER = getenv("SQL_USER")
SQL_PASSWORD = getenv("SQL_PASSWORD")

def getDatabaseConnection():
	return psycopg.connect(f"dbname={DB_NAME} host={DB_HOST} user={SQL_USER} password={SQL_PASSWORD}")

conn = getDatabaseConnection()
cur = conn.cursor()

def addNewProduct():
	fields = {
		"name" : "",
		"desc" : "",
		"price" : 0,
		"avail" : 0,
		"virtAvail" : 0,
		"categoryId" : 0,
		"companyId" : 0,
		"unit" : "",
		"amount" : 0
	}

	for it in fields.keys():
		if it == "virtAvail":
			fields[it] = fields["avail"]
			continue

		if it == "categoryId":													# todo move this to a separate function
			cur.execute("SELECT * FROM kategoria;")
			if cur.fetchone() == None:
				opt = input("no categories found, [a]dd / [c]ancel? ")
				if opt == 'a' or opt == 'A':
					addNewCategory()
				else:
					return

			cur.execute("SELECT * FROM kategoria;")
			print(cur.fetchall())

		if it == "companyId":
			cur.execute("SELECT * FROM producent WHERE id_kat = (%s);", list(fields["categoryId"]))
			if cur.fetchone() == None:
				opt = input("no companies found, [a]dd / [c]ancel? ")
				if opt == 'a' or opt == 'A':
					addNewCompany()
				else:
					return

			cur.execute("SELECT * FROM producent WHERE id_kat = (%s);", list(fields["categoryId"]))
			print(cur.fetchall())


		fields[it] = input(f"{it}: ")

	cur.execute("INSERT INTO produkt (nazwa, opis, cena, stan_rzeczywisty, stan_wirtualny, id_kat, id_firmy, jednostka, ilosc) VALUES "
	"(%s, %s, %s, %s, %s, %s, %s, %s, %s);", list(fields.values()))
	conn.commit()

def addNewCategory():
	# conn = getDatabaseConnection()
	# cur = conn.cursor()

	fields = {
		"name" : "",
		"desc" : ""
	}

	for it in fields.keys():
		fields[it] = input(f"{it}: ")

	cur.execute("INSERT INTO kategoria (nazwa, opis) VALUES (%s, %s);", list(fields.values()))
	conn.commit()

def addNewCompany():
	fields = {
		"name" : "",
		"desc" : "",
		"categoryId" : 0
	}

	for it in fields.keys():
		if it == "categoryId":													# same as above
			cur.execute("SELECT * FROM kategoria;")
			if cur.fetchone() == None:
				opt = input("no categories found, [a]dd / [c]ancel? ")
				if opt == 'a' or opt == 'A':
					addNewCategory()
				else:
					return
				
			cur.execute("SELECT * FROM kategoria;")
			print(cur.fetchall())
				
		fields[it] = input(f"{it}: ")

	cur.execute("INSERT INTO producent (nazwa, opis, id_kat) VALUES (%s, %s, %s);", list(fields.values()))
	conn.commit()


while True:
	opt = int(input("1. new product / 2. new category / 3. new company "))
	if opt == 1:
		addNewProduct()
	elif opt == 2:
		addNewCategory()
	elif opt == 3:
		addNewCompany()
	else:
		print("invalid option\n\n")