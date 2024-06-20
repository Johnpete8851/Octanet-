class User:
    def __init__(self, user_id, pin, balance=0):
        self.user_id = user_id
        self.pin = pin
        self.balance = balance
        self.transactions = []

    def verify_pin(self, pin):
        return self.pin == pin

    def record_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_transactions(self):
        return self.transactions


class ATM:
    def __init__(self):
        self.users = {}
        self.current_user = None

    def add_user(self, user):
        self.users[user.user_id] = user

    def authenticate_user(self, user_id, pin):
        user = self.users.get(user_id)
        if user and user.verify_pin(pin):
            self.current_user = user
            return True
        return False

    def get_balance(self):
        return self.current_user.balance

    def withdraw(self, amount):
        if amount > self.current_user.balance:
            print("Insufficient funds.")
            return False
        self.current_user.balance -= amount
        self.current_user.record_transaction(f"Withdraw: ${amount}")
        return True

    def deposit(self, amount):
        self.current_user.balance += amount
        self.current_user.record_transaction(f"Deposit: ${amount}")

    def transfer(self, to_user_id, amount):
        if amount > self.current_user.balance:
            print("Insufficient funds.")
            return False
        to_user = self.users.get(to_user_id)
        if not to_user:
            print("Recipient user not found.")
            return False
        self.current_user.balance -= amount
        to_user.balance += amount
        self.current_user.record_transaction(f"Transfer: ${amount} to {to_user_id}")
        to_user.record_transaction(f"Received: ${amount} from {self.current_user.user_id}")
        return True

    def transaction_history(self):
        for transaction in self.current_user.get_transactions():
            print(transaction)


class ATMApp:
    def __init__(self):
        self.atm = ATM()

    def run(self):
        print("Welcome to the ATM!")
        while True:
            print("\n1. Create new account")
            print("2. Login to existing account")
            choice = input("Choose an option: ")

            if choice == '1':
                self.create_account()
            elif choice == '2':
                if self.login():
                    self.show_menu()
            else:
                print("Invalid option, please try again.")

    def create_account(self):
        user_id = input("Create User ID: ")
        pin = input("Create PIN: ")
        if user_id in self.atm.users:
            print("User ID already exists. Please choose a different User ID.")
        else:
            self.atm.add_user(User(user_id, pin))
            print("Account created successfully. You can now login.")

    def login(self):
        user_id = input("Enter User ID: ")
        pin = input("Enter PIN: ")

        if not self.atm.authenticate_user(user_id, pin):
            print("Invalid User ID or PIN.")
            return False
        return True

    def show_menu(self):
        while True:
            print("\n1. Transaction History")
            print("2. Withdraw")
            print("3. Deposit")
            print("4. Transfer")
            print("5. Quit")
            choice = input("Choose an option: ")

            if choice == '1':
                self.atm.transaction_history()
            elif choice == '2':
                amount = float(input("Enter amount to withdraw: "))
                if self.atm.withdraw(amount):
                    print("Withdrawal successful.")
                else:
                    print("Withdrawal failed.")
            elif choice == '3':
                amount = float(input("Enter amount to deposit: "))
                self.atm.deposit(amount)
                print("Deposit successful.")
            elif choice == '4':
                to_user_id = input("Enter recipient User ID: ")
                amount = float(input("Enter amount to transfer: "))
                if self.atm.transfer(to_user_id, amount):
                    print("Transfer successful.")
                else:
                    print("Transfer failed.")
            elif choice == '5':
                print("Thank you for using the ATM. Goodbye!")
                break
            else:
                print("Invalid option, please try again.")


if __name__ == "__main__":
    app = ATMApp()
    app.run()
