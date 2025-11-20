import psycopg
from dotenv import load_dotenv
from os import getenv
from typing import Optional, cast, LiteralString
from colorama import Fore, Style, init
from datetime import datetime, date

init(autoreset=True)
load_dotenv()

DB_NAME = getenv("DB_NAME")
DB_HOST = getenv("DB_HOST")
SQL_USER = getenv("SQL_USER")
SQL_PASSWORD = getenv("SQL_PASSWORD")

def getDatabaseConnection():
	return psycopg.connect(f"dbname={DB_NAME} host={DB_HOST} user={SQL_USER} password={SQL_PASSWORD}")

conn = getDatabaseConnection()
cur = conn.cursor()

def separator(title: str = ""):
	print(Fore.CYAN + "\n" + "═" * 60)
	if title:
		print(Fore.WHITE + f" {title.upper()} ".center(60))
		print(Fore.CYAN + "═" * 60 + Style.RESET_ALL)

def show_table(rows, label="Items"):
	if not rows:
		print(Fore.YELLOW + f"No {label.lower()} found.")
		return
	print(Fore.CYAN + f"\n{label}:")
	for row in rows:
		if len(row) >= 2:
			print(Fore.WHITE + f"  [{row[0]}] {row[1]}")
	print()

def addNewProduct():
	separator("Add New Product")
	fields = {
		"name": "",
		"desc": "",
		"price": 0,
		"avail": 0,
		"virtAvail": 0,
		"categoryId": 0,
		"companyId": 0,
		"unit": "",
		"amount": 0
	}

	for it in fields.keys():
		if it == "virtAvail":
			fields[it] = fields["avail"]
			continue

		if it == "categoryId":
			cur.execute("SELECT id_kat, nazwa FROM kategoria;")
			cats = cur.fetchall()
			if not cats:
				opt = input(Fore.YELLOW + "⚠️ No categories found, add one? (y/n): " + Fore.WHITE)
				if opt.lower() == "y":
					addNewCategory()
				else:
					return
			cur.execute("SELECT id_kat, nazwa FROM kategoria;")
			show_table(cur.fetchall(), "Available categories")

		if it == "companyId":
			cur.execute("SELECT id_firmy, nazwa FROM producent;")
			comps = cur.fetchall()
			if not comps:
				opt = input(Fore.YELLOW + "⚠️ No companies found, add one? (y/n): " + Fore.WHITE)
				if opt.lower() == "y":
					addNewCompany()
				else:
					return
			cur.execute("SELECT id_firmy, nazwa FROM producent;")
			show_table(cur.fetchall(), "Available companies")

		fields[it] = input(Fore.WHITE + f"{it}: ")

	cur.execute(
		"INSERT INTO produkt (nazwa, opis, cena, stan_rzeczywisty, stan_wirtualny, id_kat, id_firmy, jednostka, ilosc) "
		"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);",
		list(fields.values()),
	)
	conn.commit()
	print(Fore.GREEN + "✅ Product successfully added!")

def addNewCategory():
	separator("Add New Category")
	fields = {"name": "", "desc": ""}
	for it in fields.keys():
		fields[it] = input(Fore.WHITE + f"{it}: ")
	cur.execute("INSERT INTO kategoria (nazwa, opis) VALUES (%s, %s);", list(fields.values()))
	conn.commit()
	print(Fore.GREEN + "✅ Category added!")

def addNewCompany():
	separator("Add New Company")
	fields = {"name": "", "desc": "", "categoryId": 0}
	for it in fields.keys():
		if it == "categoryId":
			cur.execute("SELECT id_kat, nazwa FROM kategoria;")
			show_table(cur.fetchall(), "Available categories")
		fields[it] = input(Fore.WHITE + f"{it}: ")
	cur.execute("INSERT INTO producent (nazwa, opis, id_kat) VALUES (%s, %s, %s);", list(fields.values()))
	conn.commit()
	print(Fore.GREEN + "✅ Company added!")

def modifyProduct():
	separator("Modify Product")
	rows = []
	while len(rows) != 1:
		product = input(Fore.WHITE + "Enter product ID or name: ").strip()
		if product.isdigit():
			cur.execute("SELECT id_prod, nazwa FROM produkt WHERE id_prod = %s;", (int(product),))
		else:
			cur.execute("SELECT id_prod, nazwa FROM produkt WHERE LOWER(nazwa) LIKE %s;", (f"%{product.lower()}%",))
		rows = cur.fetchall()
		if len(rows) == 0:
			print(Fore.RED + "❌ Cannot find product.")
		elif len(rows) > 1:
			print(Fore.YELLOW + "Multiple matches:")
			for row in rows:
				print(f"[{row[0]}] {row[1]}")

	print(Fore.CYAN + f"Selected {rows[0][1]}")
	opt = input(Fore.WHITE + "Edit (e) / Delete (d): ")

	if opt.lower() == "d":
		cur.execute("DELETE FROM produkt WHERE id_prod = %s;", (rows[0][0],))
		conn.commit()
		print(Fore.GREEN + "🗑️ Product deleted.")
		return
	
	fields: dict[str, Optional[str]] = {
		"opis": None,
		"cena": None,
		"stan_rzeczywisty": None,
		"stan_wirtualny": None,
	}
	updateQuery = "UPDATE produkt SET "
	updateValues = []
	for it in fields.keys():
		newValue = input(Fore.WHITE + f"New {it} (leave empty to skip): ")
		if newValue:
			updateQuery += f"{it} = %s, "
			updateValues.append(newValue)

	updateQuery = updateQuery.rstrip(", ") + " WHERE id_prod = %s;"
	updateValues.append(rows[0][0])
	if len(updateValues) == 1:
		print(Fore.RED + "No changes specified.")
		return
	cur.execute(cast(LiteralString, updateQuery), updateValues)
	conn.commit()
	print(Fore.GREEN + "✅ Product updated!")

def getAllOrders():
	separator("All Orders")
	limit = input("Number of recent orders (default 20): ")
	if not limit.isdigit():
		limit = 20
	cur.execute("SELECT * FROM zamowienia ORDER BY id_zam DESC LIMIT %s;", (int(limit),))
	print("  ID  |  ID_KLIENTA  |    DATA    |    STATUS    |  KWOTA  ")
	for row in cur.fetchall():
		print(f"{row[0]:^6}|{row[1]:^14}|{row[2].strftime("%Y-%m-%d"):^12}|{row[3]:^14}|{row[4]:^9}")

def getUnrealizedOrders():
	separator("Pending Orders")
	cur.execute("SELECT * FROM zamowienia WHERE status LIKE 'OCZEKUJĄCE' ORDER BY id_zam;")
	print("  ID  |  ID_KLIENTA  |    DATA    |  KWOTA  ")
	for row in cur.fetchall():
		print(f"{row[0]:^6}|{row[1]:^14}|{row[2].strftime("%Y-%m-%d"):^12}|{row[4]:^9}")

def getOrderDetails():
	separator("Order Details")
	orderId = input("Enter order ID: ")
	if not orderId.isdigit():
		print(Fore.RED + "❌ Invalid ID.")
		return
	cur.execute(
		"SELECT p.nazwa, s.ilosc, s.cena FROM szczegolyzam s JOIN produkt p ON s.id_prod = p.id_prod WHERE id_zam = %s;",
		(orderId,),
	)
	rows = cur.fetchall()
	if not rows:
		print(Fore.YELLOW + "⚠️ No details found.")
		return
	for row in rows:
		print(f"{row[0]} x{row[1]} — {row[2]} zł")
	cur.execute("SELECT * FROM zamowienia WHERE id_zam = %s;", (orderId,))
	print(Fore.CYAN + f"Summary: {cur.fetchone()}")
	opt = input("[M]ark as realized / [C]ancel order / [E]xit: ")
	if opt.lower() == "m":
		for row in rows:
			cur.execute("UPDATE produkt SET stan_rzeczywisty = stan_rzeczywisty - %s WHERE nazwa = %s", (row[1], row[0]))
		cur.execute("UPDATE zamowienia SET status = 'zrealizowane' WHERE id_zam = %s;", (orderId,))
		conn.commit()
		print(Fore.GREEN + "✅ Order marked as realized.")
	elif opt.lower() == "c":
		cur.execute("DELETE FROM szczegolyzam WHERE id_zam = %s;", (orderId,))
		cur.execute("DELETE FROM zamowienia WHERE id_zam = %s;", (orderId,))
		conn.commit()
		print(Fore.RED + "🗑️ Order canceled.")
	else:
		pass

def checkAvailability():
	separator("Check Stock")
	productId = input("Enter product ID (leave empty for all): ")
	if productId:
		if not productId.isdigit():
			print(Fore.RED + "❌ Invalid ID.")
			return
		cur.execute("SELECT nazwa, stan_rzeczywisty, stan_wirtualny FROM produkt WHERE id_prod = %s;", (int(productId),))
		row = cur.fetchone()
		print(row if row else Fore.YELLOW + "⚠️ No product found.")
	else:
		cur.execute("SELECT id_prod, nazwa, stan_rzeczywisty, stan_wirtualny FROM produkt;")
		print("  ID  |          NAZWA          |STAN RZECZYWISTY|STAN WIRTUALNY")
		for row in cur.fetchall():
			print(f"{row[0]:^6}|{row[1]:^25}|{row[2]:^16}|{row[3]:^14}")

def lookupUsr():
	separator("User data")
	userId = input("Enter account ID: ")
	if not userId.isdigit():
		print(Fore.RED + "❌ Invalid ID.")
		return
	cur.execute(
		"SELECT * FROM klient WHERE id_klienta = %s;",
		(userId,),
	)
	row = cur.fetchone()
	print(f"{row[0]}, {row[1]} {row[2]}, {row[6]}, {row[7]}")

def grantAdminPrivileges():
	separator("Grant admin privileges")
	userId = input("Enter account ID: ")
	if not userId.isdigit():
		print(Fore.RED + "❌ Invalid ID.")
		return
	conf = input("Type in \"yes\" to confirm. ➤ ")
	if conf == "yes":
		cur.execute(
			"UPDATE klient SET is_admin = true WHERE id_klienta = %s;",
			(userId,),
		)
		conn.commit()
		print(Fore.GREEN + "Privileges granted.")
	else:
		print(Fore.RED + "Canceling...")

def deleteUsrAccount():
	separator("User account deletion")
	userId = input("Enter account ID: ")
	if not userId.isdigit():
		print(Fore.RED + "❌ Invalid ID.")
		return
	conf = input("Type in \"yes\" to confirm. ➤ ")
	if conf == "yes":
		cur.execute(
			"DELETE FROM klient WHERE id_klienta = %s;",
			(userId,),
		)
		conn.commit()
		print(Fore.GREEN + "Account deleted.")
	else:
		print(Fore.RED + "Canceling...")

def userMgmtMenu():
	separator("User Management Menu")
	print(Fore.WHITE + "[1] Lookup user\n[2] Grant admin status\n[3] Delete account\n[0] Back")
	try:
		opt = int(input("➤ Choose: "))
	except ValueError:
		print(Fore.RED + "❌ Invalid input.")
		return
	if opt == 1:
		lookupUsr()
	elif opt == 2:
		grantAdminPrivileges()
	elif opt == 3:
		deleteUsrAccount()
	elif opt == 0:
		return
	else:
		print(Fore.RED + "❌ Invalid option.")


def addingMenu():
	separator("Add Menu")
	print(Fore.WHITE + "[1] New product\n[2] New category\n[3] New company\n[0] Back")
	try:
		opt = int(input("➤ Choose: "))
	except ValueError:
		print(Fore.RED + "❌ Invalid input.")
		return
	if opt == 1:
		addNewProduct()
	elif opt == 2:
		addNewCategory()
	elif opt == 3:
		addNewCompany()
	elif opt == 0:
		return
	else:
		print(Fore.RED + "❌ Invalid option.")

def ordersMenu():
	separator("Orders Menu")
	print(Fore.WHITE + "[1] All orders\n[2] Pending orders\n[3] Order details\n[0] Back")
	try:
		opt = int(input("➤ Choose: "))
	except ValueError:
		print(Fore.RED + "❌ Invalid input.")
		return
	if opt == 1:
		getAllOrders()
	elif opt == 2:
		getUnrealizedOrders()
	elif opt == 3:
		getOrderDetails()
	elif opt == 0:
		return
	else:
		print(Fore.RED + "❌ Invalid option.")

def adminPanel():
	separator("Admin Panel")
	conn = getDatabaseConnection()
	cur = conn.cursor()
	while True:
		print(
			Fore.YELLOW
			+ "\n[1] Add new\n[2] Modify product\n[3] Check availability\n[4] Orders\n[5] Account management\n[0] Exit"
		)
		try:
			opt = int(input(Fore.CYAN + "➤ Choose: " + Fore.WHITE))
		except ValueError:
			print(Fore.RED + "❌ Invalid input.")
			continue
		if opt == 1:
			addingMenu()
		elif opt == 2:
			modifyProduct()
		elif opt == 3:
			checkAvailability()
		elif opt == 4:
			ordersMenu()
		elif opt == 5:
			userMgmtMenu()
		elif opt == 0:
			print(Fore.MAGENTA + "👋 Exiting admin panel...")
			break
		else:
			print(Fore.RED + "❌ Invalid option.")
	cur.close()
	conn.close()

if __name__ == "__main__":
	adminPanel()
