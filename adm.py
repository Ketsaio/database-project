import psycopg
from dotenv import load_dotenv
from os import getenv
from typing import Optional, cast, LiteralString

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

def modifyProduct():
	rows = []
	
	while len(rows) != 1:
		product = input("Enter product ID or name: ").strip()
		if product.isdigit():
			cur.execute("SELECT id_prod, nazwa FROM produkt WHERE id_prod = %s;", (int(product),))
		else:
			cur.execute("SELECT id_prod, nazwa FROM produkt WHERE LOWER(nazwa) LIKE %s;", (f"%{product.lower()}%",))
		rows = cur.fetchall()

		if len(rows) == 0:
			print("Cannot find product with given ID or name.")
		elif len(rows) > 1:
			print("Found multiple matches:")
			for row in rows:
				print(row)
			print("Please refine your search.")

	prodId = rows[0][0]
	print(rows[0])
	opt = input(f"selected {rows[0][1]}, [e]dit / [d]elete? ")

	if opt == 'd' or opt == 'D':
		cur.execute("DELETE FROM produkt WHERE id_prod = %s;", (prodId,))
		conn.commit()
		return
	
	fields: dict[str, Optional[str]] = {
		"opis" : None,
		"cena" : None,
		"stan_rzeczywisty" : None,
		"stan_wirtualny" : None,
	}
	
	updateQuery = "UPDATE produkt SET "
	updateValues = []
	for it in fields.keys():
		newValue = input(f"new {it} (leave empty to keep current): ")
		if newValue != "":
			updateQuery += f"{it} = %s, "
			updateValues.append(newValue)
	

	updateQuery = updateQuery.rstrip(", ") + " WHERE id_prod = %s;"
	updateValues.append(prodId)

	cur.execute(cast(LiteralString, updateQuery), updateValues)
	conn.commit()

while True:
	opt = int(input("1. new product / 2. new category / 3. new company / 4. modify product / 5. exit: "))
	if opt == 1:
		addNewProduct()
	elif opt == 2:
		addNewCategory()
	elif opt == 3:
		addNewCompany()
	elif opt == 4:
		modifyProduct()
	elif opt == 5:
		break
	else:
		print("invalid option\n\n")