from signin import Account
from adm import adminPanel
from client import Client

def main():
	acc = Account()
	while True:
		while acc.signIn() == True:
			print(f"welcome {acc.username}")
			if acc.getStatus() == "admin":
				adminPanel()
			else:
				c = Client()
				c.main_loop()
				
if __name__ == "__main__":
	main()