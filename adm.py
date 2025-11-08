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

	print(rows[0])
	opt = input(f"selected {rows[0][1]}, [e]dit / [d]elete? ")

	if opt == 'd' or opt == 'D':
		cur.execute("DELETE FROM produkt WHERE id_prod = %s;", (rows[0][0],))
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
	updateValues.append(rows[0][0])

	cur.execute(cast(LiteralString, updateQuery), updateValues)
	conn.commit()

def getAllOrders():
	limit = input("number of recent orders to fetch (default 20): ")
	if limit.isdigit() is False:
		limit = 20

	cur.execute("SELECT * FROM zamowienia ORDER BY id_zam DESC LIMIT %s;", (int(limit),))	
		
	for row in cur.fetchall():
		print(row)

def getUnrealizedOrders():
	cur.execute("SELECT * FROM zamowienia WHERE status LIKE 'niezrealizowane' ORDER BY id_zam;")
		
	for row in cur.fetchall():
		print(row)

def getOrderDetails():
	orderId = input("Enter order ID: ")
	if orderId.isdigit() is False:
		print("invalid order ID")
		return
	
	cur.execute("SELECT * FROM szczegolyzam WHERE id_zam = %s;", (orderId,))

	if cur.rowcount == 0:
		print("no details found for given order ID")
		return
		
	for row in cur.fetchall():
		print(row)

	cur.execute("SELECT * FROM zamowienia WHERE id_zam = %s;", (orderId,))
	print(cur.fetchone())

	opt = input("[m]ark as realized / [c]ancel: ")
	if opt == 'm' or opt == 'M':
		cur.execute("UPDATE zamowienia SET status = 'zrealizowane' WHERE id_zam = %s;", (orderId,))
		conn.commit()
		print("order marked as realized")

	elif opt == 'c' or opt == 'C':
		cur.execute("DELETE FROM szczegolyzam WHERE id_zam = %s;", (orderId,))
		cur.execute("DELETE FROM zamowienia WHERE id_zam = %s;", (orderId,))
		conn.commit()
		print("order canceled")

def checkAvailability():
	productId = input("Enter product ID or leave blank for all: ")

	if productId != "":
		if productId.isdigit() is False:
			print("invalid product ID")
			return
		
		cur.execute("SELECT nazwa, stan_rzeczywisty, stan_wirtualny FROM produkt WHERE id_prod = %s;", (int(productId),))
		row = cur.fetchone()
		if row is None:
			print("no product found with given ID")
		else:
			print(row)
	
	else:
		cur.execute("SELECT nazwa, stan_rzeczywisty, stan_wirtualny FROM produkt;")
		for row in cur.fetchall():
			print(row)

def addingMenu():
	opt = int(input("1. new product / 2. new category / 3. new company / 4. back: "))
	if opt == 1:
		addNewProduct()
	elif opt == 2:
		addNewCategory()
	elif opt == 3:
		addNewCompany()
	elif opt == 4:
		return
	else:
		print("invalid option\n\n")

def ordersMenu():
	opt = int(input("1. get all orders / 2. get unrealized orders / 3. get order details / 4. back: "))
	if opt == 1:
		getAllOrders()
	elif opt == 2:
		getUnrealizedOrders()
	elif opt == 3:
		getOrderDetails()
	elif opt == 4:
		return
	else:
		print("invalid option\n\n")


def mainMenu():
	while True:
		opt = int(input("1. add new / 2. modify product / 3. check availability / 4. orders / 5. exit: "))
		if opt == 1:
			addingMenu()
		elif opt == 2:
			modifyProduct()
		elif opt == 3:
			checkAvailability()
		elif opt == 4:
			ordersMenu()
		elif opt == 5:
			print("exiting...")
			break
		else:
			print("invalid option\n\n")

	cur.close()
	conn.close()

if __name__ == "__main__":
	mainMenu()