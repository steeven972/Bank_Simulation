import datetime
import random


def generate_iban():
    country_code = "FR"
    control_key = f"{random.randint(0, 99):02d}"
    bank_code = "12345"
    branch_code = "67890"
    account_number = f"{random.randint(0, 99999999999):011d}"
    return f"{country_code}{control_key}{bank_code}{branch_code}{account_number}"

class BankAccount:
    def __init__(self, id, IBAN, balance, history):
        self.id = id
        self.iban = IBAN
        self.balance = balance
        self.history = history or []
        self.iban = IBAN or generate_iban()
        self.currency = "EUR"
        
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            
            self.history.append({"Deposited": amount, "Date": datetime.datetime.now().isoformat()})

        else:
            return "Deposit amount must be positive."
        
    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.history.append({"Withdrew": amount, "Date": datetime.datetime.now().isoformat()})
        else:
            return "Insufficient funds or invalid withdrawal amount."
    
    def transfer(self, amount, target_account):
        if amount > 0 and amount <= self.balance:
            self.withdraw(amount)
            target_account.deposit(amount)
            return "Transfer successful."
        else:
            return "Insufficient funds or invalid transfer amount."
    def get_balance(self):
        return self.balance

    def get_history(self):
        return self.history
    
    def show_history(self):
        for transaction in self.history:
            if transaction.get("Deposited"):
                print(f"Deposited: {transaction.get('Deposited') } {self.currency} at {transaction.get('Date')}")
            else:
                print(f"Withdrew: {-transaction.get('Withdrew')} {self.currency} at {transaction.get('Date')}")

    def get_id(self):
        return self.id
    
    def get_user(self):
        return self.user
    
    def get_iban(self):
        return self.iban
    







