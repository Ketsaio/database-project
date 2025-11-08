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

class Account:
	def __init__(self):
		self.account_id = 0
		self.username = ""
		self.admStatus = False

	def signIn(self) -> bool:
		usr = input("username: ")
		pwd = input("password: ")

		cur.execute("SELECT user_id, username, is_admin FROM users WHERE username LIKE %s AND password LIKE %s;", [usr, pwd])

		if cur.rowcount == 0:
			print("account not found")
			return False

		else:
			res = cur.fetchone()
			self.account_id = res[0]
			self.username = res[1]
			self.admStatus = res[2]

			return True
		
	def getStatus(self) -> str:
		if self.admStatus:
			return "admin"
		else:
			return "usr"
