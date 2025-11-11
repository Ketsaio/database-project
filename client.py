import psycopg as ps
from dotenv import load_dotenv
from os import getenv
from datetime import date
from time import sleep
from colorama import Fore, Style, init

init(autoreset=True)
load_dotenv()


def client_start_up(client_id: int):
    client = Client(client_id)
    client.main_loop()


def separator(title: str = ""):
    print(Fore.CYAN + "\n" + "─" * 70)
    if title:
        print(Fore.WHITE + f" {title.upper()} ".center(70))
        print(Fore.CYAN + "─" * 70 + Style.RESET_ALL)


class Client:
    def __init__(self, client_id: int):
        self.DB_NAME = getenv("DB_NAME")
        self.SQL_USER = getenv("SQL_USER")
        self.SQL_PASSWORD = getenv("SQL_PASSWORD")
        self.DB_HOST = getenv("DB_HOST")

        self.cart = {}
        self.add_to_query = []
        self.QUERY = self.default_query()
        self.cur = None
        self.filters_check = {1: None, 2: None, 3: None, 4: None, 5: None}
        self.client_id = client_id

    def main_loop(self):
        try:
            with ps.connect(
                f"dbname={self.DB_NAME} user={self.SQL_USER} password={self.SQL_PASSWORD} host={self.DB_HOST}"
            ) as conn:
                with conn.cursor() as cur:
                    self.cur = cur
                    separator("Welcome to our shop")

                    while True:
                        try:
                            self.print_from_db(self.QUERY, True)

                            print(
                                Fore.YELLOW
                                + "\nWhat would you like to do?"
                                + Fore.WHITE
                            )
                            print("[1] Filter products")
                            print("[2] Clear filters")
                            print("[3] Manage cart")
                            print("[4] View order history")
                            print("[0] Exit")

                            choice = input(Fore.CYAN + "➤ Choose: " + Fore.WHITE)
                            if not choice.isdigit():
                                print(Fore.RED + "❌ Please enter a number.")
                                continue

                            x = int(choice)
                            if x == 1:
                                self.filters()
                            elif x == 2:
                                self.QUERY = self.default_query()
                                self.add_to_query.clear()
                                self.filters_check = {1: None, 2: None, 3: None, 4: None, 5: None}
                                print(Fore.GREEN + "✅ Filters cleared.")
                            elif x == 3:
                                self.cart_func()
                            elif x == 4:
                                self.history()
                            elif x == 0:
                                print(Fore.MAGENTA + "👋 Exiting shop...")
                                return
                            else:
                                print(Fore.RED + "❌ Choose between 1 and 5.")
                        except (ValueError, TypeError):
                            print(Fore.RED + "❌ Invalid input.")
        except Exception as e:
            print(Fore.RED + f"❌ Database error: {e}")

    def default_query(self):
        return "SELECT produkt.* FROM produkt JOIN kategoria ON produkt.id_kat = kategoria.id_kat JOIN producent ON produkt.id_firmy = producent.id_firmy WHERE (produkt.stan_wirtualny IS NOT NULL AND produkt.stan_wirtualny > 0)"

    def print_from_db(self, what_to_print, mainQUERY):
        if mainQUERY:
            self.cur.execute((what_to_print + " ORDER BY id_prod LIMIT 20;"), tuple(self.add_to_query))
            print(Fore.CYAN + "\nAvailable products:\n" + Style.RESET_ALL)
            for record in self.cur.fetchall():
                cost = f"{record[3]:>7.2f} zł"
                print(
                    f'{str(record[0])+".":<3} {record[1]:<25} | {record[2]:^56} | {cost:>8} | {record[5]:>3} {record[8]}'
                )
        else:
            self.cur.execute(what_to_print + ";")
            rows = self.cur.fetchall()
            for row in rows:
                print(f"  {row[0]}")

    def filters(self):
        separator("Filters")
        print("Choose your filter:")
        print("[1] Name")
        print("[2] Category")
        print("[3] Producer")
        print("[4] Price range")

        try:
            wybor = int(input(Fore.CYAN + "➤ Select: " + Fore.WHITE))
            if wybor < 1 or wybor > 4:
                print(Fore.RED + "❌ Invalid option.")
                return

            if wybor == 1:
                name = input("Enter name: ")
                QUERY_HOLDER = " produkt.nazwa LIKE %s"
                self.add_to_query.append(f"%{name}%")
                self.filters_check[1] = len(self.add_to_query) - 1

            elif wybor == 2:
                print(Fore.CYAN + "\nAvailable categories:" + Fore.WHITE)
                self.cur.execute("SELECT id_kat, nazwa FROM kategoria ORDER BY id_kat;")
                categories = self.cur.fetchall()
                if not categories:
                    print(Fore.YELLOW + "⚠️ No categories found.")
                    return
                for cid, cname in categories:
                    print(f"  [{cid}] {cname}")

                try:
                    cat_id = int(input(Fore.CYAN + "➤ Choose category ID: " + Fore.WHITE))
                except ValueError:
                    print(Fore.RED + "❌ Invalid input.")
                    return

                valid_ids = [c[0] for c in categories]
                if cat_id not in valid_ids:
                    print(Fore.RED + "❌ No such category ID.")
                    return

                QUERY_HOLDER = " kategoria.id_kat = %s"
                self.add_to_query.append(cat_id)
                self.filters_check[2] = len(self.add_to_query) - 1

            elif wybor == 3:
                print(Fore.CYAN + "\nAvailable producers:" + Fore.WHITE)
                self.cur.execute("SELECT id_firmy, nazwa FROM producent ORDER BY id_firmy;")
                producers = self.cur.fetchall()
                if not producers:
                    print(Fore.YELLOW + "⚠️ No producers found.")
                    return
                for pid, pname in producers:
                    print(f"  [{pid}] {pname}")

                try:
                    prod_id = int(input(Fore.CYAN + "➤ Choose producer ID: " + Fore.WHITE))
                except ValueError:
                    print(Fore.RED + "❌ Invalid input.")
                    return

                valid_ids = [p[0] for p in producers]
                if prod_id not in valid_ids:
                    print(Fore.RED + "❌ No such producer ID.")
                    return

                QUERY_HOLDER = " producent.id_firmy = %s"
                self.add_to_query.append(prod_id)
                self.filters_check[3] = len(self.add_to_query) - 1

            elif wybor == 4:
                try:
                    print("Enter two numbers (e.g. 10 100)")
                    x, y = sorted(map(float, input("> ").split()))
                except ValueError:
                    print(Fore.RED + "❌ Invalid range.")
                    return
                QUERY_HOLDER = " produkt.cena BETWEEN %s AND %s"
                self.add_to_query.extend([x, y])
                self.filters_check[4] = len(self.add_to_query) - 2
                self.filters_check[5] = len(self.add_to_query) - 1

            self.QUERY += " AND" + QUERY_HOLDER
            print(Fore.GREEN + "✅ Filter added.")

        except (ValueError, TypeError):
            print(Fore.RED + "❌ Invalid input.")

    def cart_func(self):
        separator("Cart Menu")
        print("[1] View cart")
        print("[2] Add item")
        print("[3] Remove item")
        print("[4] Checkout")
        try:
            choice = input(Fore.CYAN + "➤ Choose: " + Fore.WHITE)
            if not choice.isdigit():
                print(Fore.RED + "❌ Invalid input.")
                return
            x = int(choice)
            if x == 1:
                self.show_cart()
            elif x == 2:
                self.add_to_cart()
            elif x == 3:
                self.remove_from_cart()
            elif x == 4:
                self.buy_out()
            else:
                print(Fore.RED + "❌ Invalid option.")
        except Exception:
            print(Fore.RED + "❌ Error reading input.")

    def show_cart(self):
        if not self.cart:
            print(Fore.YELLOW + "\n🛒 Your cart is empty.")
            return
        print(Fore.CYAN + "\nYour cart:\n" + Fore.WHITE)
        for k, v in self.cart.items():
            self.cur.execute("SELECT nazwa, jednostka FROM produkt WHERE id_prod = %s;", (k,))
            name, unit = self.cur.fetchone()
            print(f"[{k:<3}] {name:<25} | {v[0]} {unit} | {v[0] * v[1]:.2f} zł")

    def add_to_cart(self):
        print("\nEnter item ID and quantity (e.g. 1 3)")
        try:
            item_id, item_quan = map(int, input("> ").split())
            self.cur.execute("SELECT stan_wirtualny, cena FROM produkt WHERE id_prod = %s AND stan_wirtualny > 0", (item_id,))
            result = self.cur.fetchone()
            if not result:
                print(Fore.RED + "❌ Invalid ID or out of stock.")
                return
            stock, price = result
            if stock < item_quan:
                print(Fore.YELLOW + f"⚠️ Only {stock} available.")
                return
            self.cart[item_id] = [item_quan, price]
            print(Fore.GREEN + "✅ Item added.")
        except (ValueError, TypeError):
            print(Fore.RED + "❌ Invalid input.")

    def remove_from_cart(self):
        if not self.cart:
            print(Fore.YELLOW + "\nCart is empty.")
            return
        self.show_cart()
        try:
            item_id = int(input("\nEnter ID to remove: "))
            if item_id in self.cart:
                del self.cart[item_id]
                print(Fore.GREEN + "✅ Removed.")
            else:
                print(Fore.RED + "❌ Item not found.")
        except ValueError:
            print(Fore.RED + "❌ Invalid input.")

    def buy_out(self):
        if not self.cart:
            print(Fore.YELLOW + "\nCart is empty.")
            return
        try:
            total_cost = sum(q * p for q, p in self.cart.values())
            blik = input(Fore.CYAN + f"💳 Enter 6-digit BLIK code (total {total_cost:.2f} zł): ")
            if len(blik) != 6 or not blik.isdigit():
                print(Fore.RED + "❌ Invalid BLIK code.")
                return
            print(Fore.YELLOW + "Processing payment...")
            sleep(2)

            self.cur.execute(
                "INSERT INTO zamowienia (id_klienta, data, status, kwota) VALUES (%s, %s, %s, %s) RETURNING id_zam",
                (self.client_id, date.today(), "OCZEKUJĄCE", total_cost),
            )
            id_zam = self.cur.fetchone()[0]

            for item_id, (quantity, price) in self.cart.items():
                self.cur.execute("SELECT nazwa, stan_wirtualny FROM produkt WHERE id_prod = %s", (item_id,))
                result = self.cur.fetchone()
                if not result:
                    print(Fore.RED + f"❌ Product {item_id} not found.")
                    continue
                name, stock = result
                if quantity > stock:
                    print(Fore.YELLOW + f"⚠️ Not enough stock for {name}.")
                    continue
                item_total = quantity * price
                self.cur.execute(
                    "INSERT INTO szczegolyzam (id_zam, id_prod, ilosc, cena) VALUES (%s, %s, %s, %s)",
                    (id_zam, item_id, quantity, item_total),
                )
                self.cur.execute(
                    "UPDATE produkt SET stan_wirtualny = stan_wirtualny - %s WHERE id_prod = %s",
                    (quantity, item_id),
                )

            self.cur.connection.commit()
            self.cart.clear()
            print(Fore.GREEN + "✅ Order completed successfully.")
        except Exception as e:
            self.cur.connection.rollback()
            print(Fore.RED + f"❌ Error: {e}")

    def history(self):
        separator("Order History")
        try:
            self.cur.execute("SELECT zamowienia.id_zam, zamowienia.data, zamowienia.status, zamowienia.kwota, szczegolyzam.id_prod, szczegolyzam.ilosc, produkt.cena, produkt.nazwa FROM zamowienia LEFT JOIN szczegolyzam ON zamowienia.id_zam = szczegolyzam.id_zam LEFT JOIN produkt ON szczegolyzam.id_prod = produkt.id_prod WHERE zamowienia.id_klienta = %s ORDER BY zamowienia.id_zam DESC, szczegolyzam.id", (self.client_id,),)
            rows = self.cur.fetchall()
            if not rows:
                print(Fore.YELLOW + "\n📦 No order history found.")
                return
            current_order = None
            for rekord in rows:
                id_zam, date_, status, total, id_prod, count, cost, name = rekord
                if id_zam != current_order:
                    current_order = id_zam
                    print(Fore.CYAN + f"\nOrder #{id_zam} ({date_}) — {status}, {total} zł")
                if id_prod:
                    print(Fore.WHITE + f"  • {name:<35} x{count:<3} {cost:.2f} zł")
        except Exception as e:
            print(Fore.RED + f"❌ Error loading history: {e}")


if __name__ == "__main__":
    separator("Client Mode")
    try:
        client_id = int(input(Fore.CYAN + "Enter client ID: " + Fore.WHITE))
        klient = Client(client_id)
        klient.main_loop()
    except ValueError:
        print(Fore.RED + "❌ Invalid client ID.")
