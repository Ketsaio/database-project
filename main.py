from signin import Account
from adm import adminPanel
from client import client_start_up
from colorama import Fore, Style, init

init(autoreset=True)

def print_banner():
	print(Fore.CYAN + "╔" + "═" * 48 + "╗")
	print(Fore.CYAN + "║" + Fore.WHITE + "      Welcome to the Secure Client System       " + Fore.CYAN + "║")
	print(Fore.CYAN + "╚" + "═" * 48 + "╝" + Style.RESET_ALL)

def main():
	acc = Account()
	print_banner()

	while True:
		print()
		print(Fore.YELLOW + "Please choose an option:")
		print(Fore.GREEN + " [1]" + Fore.WHITE + " Sign In")
		print(Fore.GREEN + " [2]" + Fore.WHITE + " Sign Up")
		print(Fore.RED + " [0]" + Fore.WHITE + " Exit")

		opt = input(Fore.CYAN + "➤ Your choice: " + Fore.WHITE)
		try:
			opt = int(opt)
		except Exception:
			print(Fore.RED + "❌ Invalid input. Please enter a number.")
			continue

		if opt == 0:
			print(Fore.MAGENTA + "👋 Goodbye!")
			break

		elif opt == 1:
			if not acc.signIn():
				continue
			print(Fore.GREEN + f"✅ Welcome, {acc.firstName}!")

			if acc.getStatus() == "admin":
				adminPanel()
			else:
				client_start_up(acc.account_id)

		elif opt == 2:
			acc.signUp()

		else:
			print(Fore.RED + "❌ Invalid option. Try again.")
			continue

if __name__ == "__main__":
	main()
