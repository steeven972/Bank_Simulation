import hashlib


class User:
    def __init__(self, id, name, surname, password, code):
        self.id = id
        self.name = name
        self.surname = surname
        self.password = password
        self.code = code
        self.accounts = {}
        
    def add_account(self, account):
        if str(account.get_id()) not in self.accounts:
            self.accounts[account.get_id()] = account
        else:
            return "Account ID already exists."
        
    def delete_account(self, account_id):
        if account_id in self.accounts:
            del self.accounts[account_id]
            return "Account deleted successfully."
        else:
            return "Account ID does not exist."
        
    def get_account(self, account_id):
        return self.accounts.get(account_id, None)
    
    def set_password(self, new_password, old_password):
        if self.verify_password(old_password):
            self.password = hashlib.sha256(new_password.encode()).hexdigest()
            return "Password updated successfully."
        else:
            return "Old password is incorrect."
        
    def verify_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest() == self.password
    
    def save_user_data(self):
        new_user_data = {
        
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "password": self.password,
            "code": self.code,
            "accounts": {acc_id: {
                "id": acc.get_id(),
                "IBAN": acc.get_iban(),
                "balance": acc.get_balance(),
                "history": acc.get_history()
            } for acc_id, acc in self.accounts.items()}
        
        }
        return new_user_data
