from tkinter import messagebox
import tkinter as tk



from backend.account import BankAccount
from backend.user import User


from utils.utils import generate_iban, hash_password

class CreateAccountFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        tk.Label(self, text="Create Account", font=("Arial", 16)).pack(pady=12)

        tk.Label(self, text="Name:").pack()
        self.entry_name = tk.Entry(self); self.entry_name.pack()
        tk.Label(self, text="Surname:").pack()
        self.entry_surname = tk.Entry(self); self.entry_surname.pack()
        tk.Label(self, text="Password:").pack()
        self.entry_password = tk.Entry(self, show="*"); self.entry_password.pack()
        tk.Label(self, text="PIN Code (3-6 digits):").pack()
        self.entry_code = tk.Entry(self, show="*"); self.entry_code.pack()

        tk.Button(self, text="Submit", command=self.submit_account).pack(pady=10)
        tk.Button(self, text="Back to Home", command=self.go_home).pack()

    def go_home(self):
        from gui.homePage import HomeFrame
        self.controller.show_frame(HomeFrame)
        
    def submit_account(self):
        name = self.entry_name.get().strip()
        surname = self.entry_surname.get().strip()
        raw_password = self.entry_password.get()
        code = self.entry_code.get().strip()

        if not (name and surname and raw_password and code):
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
            return
        if not (code.isdigit() and 3 <= len(code) <= 6):
            messagebox.showerror("Erreur", "Le code PIN doit être numérique (3 à 6 chiffres).")
            return

        password = hash_password(raw_password)
        self.controller.load_users()
        for u in self.controller.users:
            if u.get("name","").lower() == name.lower() and u.get("surname","").lower() == surname.lower():
                messagebox.showwarning("Attention", "Utilisateur déjà existant.")
                return

        new_id = self.controller.next_user_id()
        account = {
            "id": 1,
            "IBAN": generate_iban(),
            "balance": 0.0,
            "history": []
        }
        '''new_user = {
            "id": new_id,
            "name": name,
            "surname": surname,
            "password": password,
            "code": code,
            "accounts": [account]
        }'''
        new_user_obj = User(new_id, name, surname, password, code)
        account_obj = BankAccount(1, None, 0.0, [])
        new_user_obj.add_account(account_obj)
        new_user_data = new_user_obj.save_user_data()

        self.controller.users.append(new_user_data)
        self.controller.save_users()

        # clear fields
        self.entry_name.delete(0, tk.END)
        self.entry_surname.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.entry_code.delete(0, tk.END)

        messagebox.showinfo("Succès", f"Compte créé pour {name} {surname} (ID: {new_id})\nIBAN: {account['IBAN']}")