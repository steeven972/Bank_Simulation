import tkinter as tk
import tkinter.messagebox as messagebox
import hashlib
import json
import os
import random
import datetime

from bankBackend import BankAccount, User

USERS_FILE = "Users.json"

def ensure_users_file():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump([], f)

def hash_password(raw: str) -> str:
    return hashlib.sha256(raw.encode()).hexdigest()

def generate_iban() -> str:
    country_code = "FR"
    control_key = f"{random.randint(0,99):02d}"
    bank_code = "12345"
    branch_code = "67890"
    account_number = f"{random.randint(0, 99999999999):011d}"
    return f"{country_code}{control_key}{bank_code}{branch_code}{account_number}"


class Interface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bank Application")
        self.geometry("460x420")

        ensure_users_file()
        self.users = []
        self.load_users()

        self.frames = {}
        for F in (HomeFrame, CreateAccountFrame, ConnectAccountFrame, DepositFrame):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomeFrame)

    def show_frame(self, frame_class):
        frame = self.frames.get(frame_class)
        if frame:
            frame.tkraise()
        else:
            print("Frame manquante:", frame_class)

    def load_users(self):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
        if not isinstance(data, list):
            data = []
        self.users = data

    def save_users(self):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.users, f, indent=4, ensure_ascii=False)
    
        self.load_users()

    def get_user_by_id(self, user_id: int):
        for u in self.users:
            if u.get("id") == user_id:
                return u
        return None

    def next_user_id(self) -> int:
        if not self.users:
            return 1
        return max(u.get("id", 0) for u in self.users) + 1


class HomeFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Bank Home", font=("Arial", 18)).pack(pady=20)
        tk.Button(self, text="Create Account", width=25, command=lambda: parent.show_frame(CreateAccountFrame)).pack(pady=8)
        tk.Button(self, text="Connect Account", width=25, command=lambda: parent.show_frame(ConnectAccountFrame)).pack(pady=8)
        tk.Button(self, text="Exit", width=25, command=parent.destroy).pack(pady=12)

class CreateAccountFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
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
        tk.Button(self, text="Back to Home", command=lambda: parent.show_frame(HomeFrame)).pack()

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
        self.parent.load_users()
        for u in self.parent.users:
            if u.get("name","").lower() == name.lower() and u.get("surname","").lower() == surname.lower():
                messagebox.showwarning("Attention", "Utilisateur déjà existant.")
                return

        new_id = self.parent.next_user_id()
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

        self.parent.users.append(new_user_data)
        self.parent.save_users()

        # clear fields
        self.entry_name.delete(0, tk.END)
        self.entry_surname.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.entry_code.delete(0, tk.END)

        messagebox.showinfo("Succès", f"Compte créé pour {name} {surname} (ID: {new_id})\nIBAN: {account['IBAN']}")

class ConnectAccountFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        tk.Label(self, text="Connect Account", font=("Arial", 16)).pack(pady=12)

        tk.Label(self, text="Identifiant (ID numérique):").pack()
        self.entry_id = tk.Entry(self); self.entry_id.pack()
        tk.Label(self, text="Password:").pack()
        self.entry_password = tk.Entry(self, show="*"); self.entry_password.pack()

        tk.Button(self, text="Submit", command=self.submit_connection).pack(pady=10)
        tk.Button(self, text="Back", command=lambda: parent.show_frame(HomeFrame)).pack()

    def submit_connection(self):
        ident = self.entry_id.get().strip()
        raw_pw = self.entry_password.get()
        if not (ident.isdigit() and raw_pw):
            messagebox.showerror("Erreur", "Identifiant numérique et mot de passe requis.")
            return
        uid = int(ident)
        pw = hash_password(raw_pw)
        self.parent.load_users()
        user = self.parent.get_user_by_id(uid)
        if user and user.get("password") == pw:
            code_frame = CodeFrame(self.parent, uid)
            code_frame.grid(row=0, column=0, sticky="nsew")
            self.parent.frames[CodeFrame] = code_frame
            self.parent.show_frame(CodeFrame)
            self.entry_id.delete(0, tk.END); self.entry_password.delete(0, tk.END)
            return
        messagebox.showerror("Erreur", "Identifiant ou mot de passe invalide.")

class CodeFrame(tk.Frame):
    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.parent = parent
        self.user_id = int(user_id)
        tk.Label(self, text="Enter PIN Code", font=("Arial", 14)).pack(pady=12)

        self.display = tk.Entry(self, font=("Arial", 18), justify="right", show="*")
        self.display.pack(pady=10, padx=10, fill="x")
        btn_frame = tk.Frame(self); btn_frame.pack()

        for i, num in enumerate(range(1, 10)):
            tk.Button(btn_frame, text=str(num), width=5, height=2, command=lambda n=num: self.add_digit(str(n))).grid(row=i//3, column=i%3, padx=5, pady=5)
        tk.Button(btn_frame, text="0", width=5, height=2, command=lambda: self.add_digit("0")).grid(row=3, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="C", width=5, height=2, command=self.clear_display).grid(row=3, column=0)
        tk.Button(btn_frame, text="OK", width=5, height=2, command=self.validate_input).grid(row=3, column=2)

        tk.Button(self, text="Back", command=lambda: parent.show_frame(ConnectAccountFrame)).pack(pady=8)

    def add_digit(self, d): self.display.insert(tk.END, d)
    def clear_display(self): self.display.delete(0, tk.END)

    def validate_input(self):
        code_value = self.display.get().strip()
        if not code_value:
            messagebox.showerror("Erreur", "Entrez le code.")
            return
        self.parent.load_users()
        user = self.parent.get_user_by_id(self.user_id)
        if user and str(user.get("code")) == code_value:
            account_frame = AccountInterface(self.parent, self.user_id)
            account_frame.grid(row=0, column=0, sticky="nsew")
            self.parent.frames[AccountInterface] = account_frame
            self.parent.show_frame(AccountInterface)
            self.clear_display()
            return
        messagebox.showerror("Erreur", "Code invalide.")
        self.clear_display()

class AccountInterface(tk.Frame):
    def __init__(self, parent, user_id):
        super().__init__(parent)
        self.parent = parent
        self.user_id = int(user_id)
        tk.Label(self, text="Account Interface", font=("Arial", 14)).pack(pady=10)

        self.parent.load_users()
        self.user = self.parent.get_user_by_id(self.user_id)
        if not self.user:
            messagebox.showerror("Erreur", "Utilisateur introuvable.")
            parent.show_frame(HomeFrame); return

        accounts = self.user.get("accounts", [])
        if not accounts:
            messagebox.showerror("Erreur", "Aucun compte trouvé."); parent.show_frame(HomeFrame); return

        self.user_account = accounts["1"]
        bal = self.user_account.get("balance", 0.0)
        tk.Label(self, text=f"User: {self.user['name']} {self.user['surname']} (ID: {self.user_id})").pack()
        self.iban_label = tk.Label(self, text=f"IBAN: {self.user_account.get('IBAN')}")
        self.iban_label.pack(pady=4)
        self.balance_label = tk.Label(self, text=f"Balance: {bal:.2f} EUR", font=("Arial",12))
        self.balance_label.pack(pady=8)

        actions = tk.Frame(self); actions.pack(pady=6)
        tk.Button(actions, text="Deposit", width=12, height=2, command=lambda uid=self.user_id: self.open_deposit(uid)).grid(row=0,column=0,padx=5)
        tk.Button(actions, text="Withdraw", width=12, height=2, command=self.open_withdraw).grid(row=0,column=1,padx=5)
        tk.Button(actions, text="Transfer", width=12, height=2, command=self.open_transfer).grid(row=0,column=2,padx=5)
        tk.Button(self, text="Disconnect", command=lambda: parent.show_frame(HomeFrame)).pack(pady=8)

    def refresh(self):
        self.parent.load_users()
        u = self.parent.get_user_by_id(self.user_id)
        if u:
            bal = u["accounts"][0].get("balance", 0.0)
            self.balance_label.config(text=f"Balance: {bal:.2f} EUR")

    def open_deposit(self, uid):
        df = self.parent.frames.get(DepositFrame)
        if df:
            df.set_user(uid)
            self.parent.show_frame(DepositFrame)
        else:
            messagebox.showerror("Erreur", "Frame dépôt indisponible.")

    def open_withdraw(self):
        messagebox.showinfo("Info", "Retrait non implémenté (à venir).")

    def open_transfer(self):
        messagebox.showinfo("Info", "Transfert non implémenté (à venir).")

class DepositFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.user_id = None
        tk.Label(self, text="Deposit", font=("Arial", 14)).pack(pady=12)

        tk.Label(self, text="Deposit Funds into Your Account").pack(pady=8)
        tk.Label(self, text="Amount to Deposit:").pack()
        self.entry_amount = tk.Entry(self); self.entry_amount.pack(pady=6)
        tk.Button(self, text="Submit", command=self.submit_deposit).pack(pady=6)
        tk.Button(self, text="Back to Account", command=self.back_to_account).pack()

    def set_user(self, user_id):
        self.user_id = int(user_id)

    def back_to_account(self):
        acc = AccountInterface(self.parent, self.user_id)
        acc.grid(row=0, column=0, sticky="nsew")
        self.parent.frames[AccountInterface] = acc
        self.parent.show_frame(AccountInterface)

    def submit_deposit(self):
        if self.user_id is None:
            messagebox.showerror("Erreur", "Aucun utilisateur sélectionné."); return
        try:
            amount = float(self.entry_amount.get().strip())
            if amount <= 0:
                messagebox.showerror("Erreur", "Le montant doit être positif."); return
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre valide."); return

        # update JSON
        self.parent.load_users()
        updated = False
        for u in self.parent.users:
            if u.get("id") == self.user_id:
                if "accounts" not in u or not u["accounts"]:
                    messagebox.showerror("Erreur", "Aucun compte pour cet utilisateur."); return
                acc = u["accounts"]["1"]
                acc["balance"] = round(acc.get("balance", 0.0) + amount, 2)
                hist = acc.get("history", [])
                hist.append({"action":"deposit", "amount": amount, "date": datetime.datetime.now().isoformat()})
                acc["history"] = hist
                new_balance = acc["balance"]
                updated = True
                break

        if not updated:
            messagebox.showerror("Erreur", "Utilisateur introuvable."); return

        self.parent.save_users()
        self.entry_amount.delete(0, tk.END)
        messagebox.showinfo("Succès", f"Dépôt de {amount:.2f} EUR effectué.\nNouveau solde : {new_balance:.2f} EUR")

        # recreate AccountInterface to refresh display
        acc_frame = AccountInterface(self.parent, self.user_id)
        acc_frame.grid(row=0, column=0, sticky="nsew")
        self.parent.frames[AccountInterface] = acc_frame
        self.parent.show_frame(AccountInterface)


if __name__ == "__main__":
    ensure_users_file()
    app = Interface()
    app.mainloop()
