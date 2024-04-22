import json

class Manager:
    def __init__(self):
        self.account_balance = 100000
        self.warehouse_products = [
            {
                "Produkt": "Płyta gipsowa",
                "Ilość": 1500,
                "Cena jednostkowa": 29.0
            }
        ]
        self.operation_list = []

    def save_data(self):
        with open("account_balance.txt", "w") as f:
            f.write(str(self.account_balance))

        with open("warehouse_products.txt", "w") as f:
            json.dump(self.warehouse_products, f)

        with open("operation_history.txt", "w") as f:
            for operation in self.operation_list:
                f.write(operation + '\n')

    def load_data(self):
        try:
            with open("account_balance.txt", "r") as f:
                self.account_balance = float(f.read())
        except FileNotFoundError:
            pass

        try:
            with open("warehouse_products.txt", "r") as f:
                self.warehouse_products = json.load(f)
        except FileNotFoundError:
            pass

        try:
            with open("operation_history.txt", "r") as f:
                self.operation_list = f.readlines()
        except FileNotFoundError:
            pass

    def execute(self, operation):
        if operation == "1":
            amount = float(input("Podaj kwotę do dodania lub odjęcia z konta: "))
            self.account_balance += amount
            if amount > 0:
                print(f"\nKwota która została dodana to: {amount}")
                self.operation_list.append(f"Dodano: {amount} do konta firmy!")
            elif amount < 0: 
                print(f"\nKwota która została odjęta to: {amount}")
                self.operation_list.append(f"Odjęto: {amount} z konta firmy!")
            else:
                print(f"\nNie dodano/odjęto żadnej kwoty!")

        elif operation == "2":
            sell_product = input("Podaj nazwę produktu: ")
            for product in self.warehouse_products:
                if product["Produkt"] == sell_product:
                    unit_price_sell = float(input("Podaj cenę jednostkową: "))
                    if unit_price_sell < 0:
                        print("Nieprawidłowa cena sprzedaży!")
                        break
                    amount_of_products_sell = int(input("Podaj ilość: "))
                    if product["Ilość"] >= amount_of_products_sell:
                        product["Ilość"] -= amount_of_products_sell
                        self.account_balance = self.account_balance + (unit_price_sell * amount_of_products_sell)
                        print("\nProdukt został sprzedany!")
                        self.operation_list.append(f"Sprzedano produkt o nazwie: {sell_product}, Cena jednostkowa: {unit_price_sell}, Ilość: {amount_of_products_sell}")
                        break
                    else:
                        print("\nBrak wystarczającej ilości produktu w magazynie!")
                        self.operation_list.append(f"Próba sprzedania produktu o nazwie: {sell_product}, którego nie ma w wystarczającej ilości w magazynie!")
                        break
            else:
                print("\nBrak produktu w magazynie!")
                self.operation_list.append(f"Próba sprzedania produktu o nazwie: {sell_product}, którego nie ma w magazynie!")
                            
        elif operation == "3":
            purchase_product = input("Podaj nazwę produktu: ")
            amount_of_products = int(input("Podaj ilość: "))
            unit_price = float(input("Podaj cenę jednostkową: "))
            if self.account_balance >= amount_of_products * unit_price:
                self.warehouse_products.append({
                    "Produkt": purchase_product,
                    "Ilość": amount_of_products,
                    "Cena jednostkowa": unit_price
                })
                self.account_balance = self.account_balance - (amount_of_products * unit_price)
                print(f"\nProdukt został dodany do magazynu!")
                self.operation_list.append(f"Zakupiono produkt o nazwie: {purchase_product}, Cena jednostkowa: {unit_price}, Ilość: {amount_of_products}")
                
            else:
                print("\nBrak wystarczających środków na koncie!")
                self.operation_list.append(f"Odrzucono zakup produktu o nazwie: {purchase_product} z powodu braku wystarczających środków na koncie!")
        
        elif operation == "4":
            print(f"\nAktualny stan konta: {self.account_balance}")
            self.operation_list.append("Sprawdzono aktualny stan konta!")

        elif operation == "5":
            print("\nStan magazynu:")
            for product in self.warehouse_products:
                print(f"{product['Produkt']}: {product['Ilość']} sztuk, Cena jednostkowa: {product['Cena jednostkowa']}")
                self.operation_list.append("Sprawdzono aktualny stan magazynu!")

        elif operation == "6":
            product_name = input("Podaj nazwę produktu: ")
            for product in self.warehouse_products:
                if product["Produkt"] == product_name:
                    print(f"\nStan magazynu dla produktu '{product_name}': {product['Ilość']} sztuk, Cena jednostkowa: {product['Cena jednostkowa']}")
                    self.operation_list.append(f"Sprawdzono aktualny stan magazynu dla produktu o nazwie: {product_name}")
                    break
            else:
                print("\nBrak produktu w magazynie!")
                self.operation_list.append(f"Sprawdzono aktualny stan magazynu dla produktu o nazwie: {product_name}, którego nie ma w magazynie!")
        
        elif operation == "7":
            start_index = input("Podaj indeks początkowy: ")
            end_index = input("Podaj indeks końcowy: ")
            if start_index == "":
                start_index = 0
            else:
                start_index = int(start_index)
            if end_index == "":
                end_index = len(self.operation_list)
            else:
                end_index = int(end_index)
            if start_index < 0 or end_index < 0 or start_index > len(self.operation_list) or end_index > len(self.operation_list) or start_index > end_index:
                print("\nBłąd: Nieprawidłowy zakres!")
                print(f"Liczba zapisanych operacji: {len(self.operation_list)}")
                return
            print("\nHistoria operacji:")
            print(self.operation_list[start_index:end_index])
        
        elif operation == "8":
            self.save_data()
            return True
        return False

    def assign(self):
        print("Witaj w programie do zarządzania kontem firmy i magazynem!")
        self.load_data()
        while True:
            operation = input("\nDostępne komendy:\n 1. Saldo\n 2. Sprzedaż\n 3. Zakup\n 4. Konto\n 5. Lista\n 6. Magazyn\n 7. Przegląd\n 8. Koniec\n")
            finished = self.execute(operation)
            if finished:
                break

manager = Manager()
manager.assign()
