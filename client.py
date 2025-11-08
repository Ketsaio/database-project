import psycopg as ps
from dotenv import load_dotenv
from os import getenv


load_dotenv()   # loads enviromental variables

class Client:
    def __init__(self):
        self.DB_NAME = getenv("DB_NAME")
        self.SQL_USER = getenv("SQL_USER")
        self.SQL_PASSWORD = getenv("SQL_PASSWORD")
        self.DB_HOST = getenv("DB_HOST")

        self.cart = {}
        self.add_to_query = []
        self.QUERY = self.default_query()
        self.cur = None
        self.filters_check = {1:None, 2:None, 3:None, 4:None, 5:None}
        #self.client_id = None -> waiting for login page

    def main_loop(self):
        try:
            with ps.connect(f"dbname={self.DB_NAME} user={self.SQL_USER} password={self.SQL_PASSWORD} host={self.DB_HOST}") as conn:
                with conn.cursor() as cur:

                    print("Welcome in our shop!")
                    self.cur = cur

                    while True:
                        try:
                            self.print_from_db(self.QUERY, True)

                            print("What would u like to do? [1 - Filter, 2 - Clear filters, 3 - Add to cart, 4 - Exit]")

                            x = int(input("> "))
                            if x < 1 or x > 4:
                                print("Choose a number between 1 and 4!")
                                continue

                            if x == 1:
                                self.filters()
                            if x == 2:
                                self.QUERY = self.default_query()
                                self.add_to_query = []
                                self.filters_check = {1:None, 2:None, 3:None, 4:None, 5:None}
                            if x == 3:
                                self.cart_func()
                            if x == 4:
                                return

                        except (ValueError, TypeError):
                            print("Please, insert a number!")
        except Exception as e:
            print(f"Something went wrong on database - script line\n{e}")

    def default_query(self):
        return "SELECT produkt.* FROM produkt JOIN kategoria ON produkt.id_kat = kategoria.id_kat JOIN producent ON produkt.id_firmy = producent.id_firmy WHERE (produkt.stan_wirtualny IS NOT NULL AND produkt.stan_wirtualny > 0)"

    def print_from_db(self, what_to_print, mainQUERY):
        if mainQUERY:
            self.cur.execute((what_to_print + " ORDER BY id_prod LIMIT 20;"), tuple(self.add_to_query))
            for record in self.cur.fetchall():
                cost = f"{record[3]:>7.2f} zł"
                print(f'{record[0]:<3} | {record[1]:^25} | {record[2]:^55} | {cost:^12} | {record[5]:>3} {record[8]}\n')
        else:
            self.cur.execute(what_to_print + ";")
            for record in self.cur.fetchall():
                print(record[0])

    def filters(self):
        print("Choose your filter!")
        print("1 - Nazwa, 2 - Kategoria, 3 - Producent, 4 - Cena")

        try:
            wybor = int(input("> "))

            if wybor < 1 or wybor > 4:
                print("Choose the correct number!")
                return

            if wybor == 1:
                name = input("Input name!\n> ")
                if self.filters_check[1] is not None:
                    self.add_to_query[self.filters_check[1]] = f"%{name}%"
                    return
                
                QUERY_HOLDER = f" produkt.nazwa LIKE %s"
                self.add_to_query.append(f"%{name}%")
                self.filters_check[1] = len(self.add_to_query) - 1

            elif wybor == 2:
                print("Available categories:")
                self.print_from_db("SELECT nazwa FROM kategoria;", False)
                category = input("Choose category!\n> ")

                if self.filters_check[2] is not None:
                    self.add_to_query[self.filters_check[2]] = category
                    return

                QUERY_HOLDER = f" kategoria.nazwa = %s"
                self.add_to_query.append(category)
                self.filters_check[2] = len(self.add_to_query) - 1

            elif wybor == 3:
                print("Available producents:")
                self.print_from_db("SELECT nazwa FROM producent;", False)
                producent = input("Choose producer!\n> ")

                if self.filters_check[3] is not None:
                    self.add_to_query[self.filters_check[3]] = producent
                    return

                QUERY_HOLDER = f" producent.nazwa = %s"
                self.add_to_query.append(producent)
                self.filters_check[3] = len(self.add_to_query) - 1


            elif wybor == 4:
                print("Specify price:")
                x, y = map(float, input("Give two numbers: 10 100\n>").split())

                if self.filters_check[4] is not None or self.filters_check[5] is not None:
                    self.add_to_query[self.filters_check[4]] = x
                    self.add_to_query[self.filters_check[5]] = y
                    return

                QUERY_HOLDER = f" produkt.cena BETWEEN %s AND %s"
                self.add_to_query.append(x)
                self.add_to_query.append(y)
                self.filters_check[4] = len(self.add_to_query) - 1
                self.filters_check[5] = len(self.add_to_query) - 1

            self.QUERY += (" AND" + QUERY_HOLDER)

            print("\n")
            
        except (ValueError, TypeError):
            print("Please, insert a number!")
    
    def cart_func(self):
        print("What do u want to do? [1 - see, 2 - add, 3 - remove]")
        try:
            x = int(input("> "))

            if x < 1 or x > 3:
                print("Choose the correct number!")
                return

            if x == 1:
                self.show_cart()
            elif x == 2:
                self.add_to_cart()
            elif x == 3:
                self.remove_from_cart()

        except (ValueError, TypeError):
            print("Please, insert a number!")

    def show_cart(self):
        if not self.cart:
            print("Your cart is empty!")
            return
        print("Your cart:")
        for k, v in self.cart.items():
            self.cur.execute("SELECT nazwa, jednostka FROM produkt WHERE id_prod = %s;", (k,))
            name, place = self.cur.fetchone()
            print(f"{k:^3} | {name:^56} | {v:^12} {place}")

    def add_to_cart(self):
        print("Choose item id and quantity, for example:\n1 3 (id: 1, quantity: 3)")
        try:
            while(True):
                item_id, item_quan = map(int, input("> ").split())
                self.cur.execute("SELECT stan_wirtualny FROM produkt WHERE id_prod = %s AND stan_wirtualny > 0",(item_id,))
            
                result = self.cur.fetchone()
            
                if not result:
                    print("Choose correct ID or item out of stock!")
                    continue
                
                available_stock = result[0]
                
                if available_stock < item_quan:
                    print(f"We don't have {item_quan} in stock! Available: {available_stock}")
                    continue

                if item_id not in self.cart:
                    self.cart[item_id] = item_quan
                else:
                    self.cart[item_id] += item_quan
                return

        except (ValueError, TypeError):
            print("Please, insert a number!")

    def remove_from_cart(self):
        try:
            item_id = int(input("Enter id to remove: "))
            if item_id in self.cart:
                del self.cart[item_id]
                print("Removed!")
            else:
                print("Item not found in cart.")
        except (ValueError, TypeError):
            print("Please, insert a number!")

if __name__ == "__main__":
    klient = Client()
    klient.main_loop()