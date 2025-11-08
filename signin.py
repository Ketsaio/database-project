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
		self.admStatus = False

	def signUp(self) -> None:
		usr = input("username: ")
		pwd = getpass.getpass("password: ")

		pwdHash = bcrypt.hashpw(pwd.encode("utf-8"), bcrypt.gensalt())

		cur.execute("INSERT INTO users (username, password) VALUES (%s, %s);", (usr, pwdHash))
		conn.commit()

		print("account created")


	def signIn(self) -> bool:
		usr = input("username: ")
		pwd = getpass.getpass("password: ")

		cur.execute("SELECT user_id, username, password, is_admin FROM users WHERE username = %s;", (usr,))
		row = cur.fetchone()

		if not row:
			print("account not found")
			return False

		user_id, username, pwdHash, is_admin = row
		if not bcrypt.checkpw(pwd.encode("utf-8"), pwdHash.encode("utf-8") if isinstance(pwdHash, str) else pwdHash):
			print("wrong password")
			return False
		
		self.account_id = user_id
		self.username = username
		self.admStatus = is_admin
		
		return True
		
	def getStatus(self) -> str:
		if self.admStatus:
			return "admin"
		else:
			return "usr"
