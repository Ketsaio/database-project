import psycopg
from dotenv import load_dotenv
from os import getenv
import getpass
import bcrypt

load_dotenv()   # loads enviromental variables

DB_NAME = getenv("DB_NAME")
DB_HOST = getenv("DB_HOST")
SQL_USER = getenv("SQL_USER")
SQL_PASSWORD = getenv("SQL_PASSWORD")

def getDatabaseConnection():
	return psycopg.connect(f"dbname={DB_NAME} host={DB_HOST} user={SQL_USER} password={SQL_PASSWORD}")

conn = getDatabaseConnection()
cur = conn.cursor()

class Account:
	def __init__(self):
		self.account_id = 0
		self.username = ""
		self.firstName = ""
		self.admStatus = False

	def signUp(self) -> None:
		usr = input("username: ")
		pwd = getpass.getpass("password: ")
		name = input("first name: ")
		lastName = input("last name: ")
		emailAddr = input("email address (optional): ")
		phoneNum = input("phone number (optional): ")

		pwdHash = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt())

		cur.execute("INSERT INTO klient (imie, nazwisko, login, haslo, email, telefon) VALUES (%s, %s, %s, %s, %s, %s);", (name, lastName, usr, pwdHash, emailAddr, phoneNum))
		conn.commit()

		print("account created")


	def signIn(self) -> bool:
		usr = input("username: ")
		pwd = getpass.getpass("password: ")

		cur.execute("SELECT id_klienta, login, haslo, is_admin, imie FROM klient WHERE login = %s;", (usr,))
		row = cur.fetchone()

		if not row:
			print("account not found")
			return False

		id_klienta, username, pwdHash, is_admin, name = row
		if not bcrypt.checkpw(pwd.encode("utf-8"), pwdHash):
			print("wrong password")
			return False
		
		self.account_id = id_klienta
		self.username = username
		self.firstName = name
		self.admStatus = is_admin

		return True
		
	def getStatus(self) -> str:
		if self.admStatus:
			return "admin"
		else:
			return "usr"
