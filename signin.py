import psycopg
from dotenv import load_dotenv
from os import getenv
import getpass
import bcrypt
from colorama import Fore, Style, init

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

class Account:
	def __init__(self):
		self.account_id = 0
		self.username = ""
		self.firstName = ""
		self.admStatus = False

	def signUp(self) -> None:
		print(Fore.CYAN + "\n╔═ Account Registration ═╗" + Style.RESET_ALL)
		usr = input(Fore.WHITE + "👤 Username: ")
		pwd = getpass.getpass("🔒 Password: ")
		confirmPwd = getpass.getpass("🔁 Confirm password: ")

		if pwd != confirmPwd:
			print(Fore.RED + "❌ Passwords do not match.")
			return
			
		name = input("🧍 First name: ")
		lastName = input("🧍 Last name: ")
		emailAddr = input("📧 Email address (optional): ")
		phoneNum = input("📞 Phone number (optional): ")

		pwdHash = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt())

		try:
			cur.execute(
				"INSERT INTO klient (imie, nazwisko, login, haslo, email, telefon) VALUES (%s, %s, %s, %s, %s, %s);",
				(name, lastName, usr, pwdHash, emailAddr, phoneNum),
			)
			conn.commit()
		except Exception:
			print(Fore.RED + "❌ Username already taken.")
			return

		print(Fore.GREEN + "✅ Account successfully created!")

	def signIn(self) -> bool:
		print(Fore.CYAN + "\n╔═ Sign In ═╗" + Style.RESET_ALL)
		usr = input(Fore.WHITE + "👤 Username: ")
		pwd = getpass.getpass("🔒 Password: ")

		cur.execute("SELECT id_klienta, login, haslo, is_admin, imie FROM klient WHERE login = %s;", (usr,))
		row = cur.fetchone()

		if not row:
			print(Fore.RED + "❌ Account not found.")
			return False

		id_klienta, username, pwdHash, is_admin, name = row
		if not bcrypt.checkpw(pwd.encode("utf-8"), pwdHash):
			print(Fore.RED + "❌ Wrong password.")
			return False
		
		self.account_id = id_klienta
		self.username = username
		self.firstName = name
		self.admStatus = is_admin

		return True
		
	def getStatus(self) -> str:
		return "admin" if self.admStatus else "usr"
