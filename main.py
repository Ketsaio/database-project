from signin import Account
from adm import adminPanel
from client import Client

def main():
	acc = Account()
	while True:
		opt = int(input("1: sign in // 2: sign up: "))	# todo add type exception handling
		if opt == 1:
			if acc.signIn():
				print(f"welcome {acc.username}")
				if acc.getStatus() == "admin":
					adminPanel()
				else:
					c = Client()
					c.main_loop()
		elif opt == 2:
			acc.signUp()
				
if __name__ == "__main__":
	main()