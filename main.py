from signin import Account
from adm import adminPanel
from client import Client

def main():
	acc = Account()
	while True:
		opt = input("1: sign in // 2: sign up: ")
		try:
			opt = int(opt)
		except Exception:
			print("invalid")
			continue

		if opt == 1:
			if not acc.signIn():
				continue
				
			print(f"welcome {acc.firstName}")
			if acc.getStatus() == "admin":
				adminPanel()
			else:
				c = Client()
				c.main_loop()

		elif opt == 2:
			acc.signUp()

		else:
			print("invalid")
			continue
				
if __name__ == "__main__":
	main()