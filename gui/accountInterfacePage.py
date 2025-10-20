import tkinter as tk
from tkinter import messagebox


from gui.depositPage import DepositFrame

class AccountInterface(tk.Frame):
    def __init__(self, parent, controller, user_id):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.user_id = int(user_id)
        tk.Label(self, text="Account Interface", font=("Arial", 14)).pack(pady=10)

        self.controller.load_users()
        self.user = self.controller.get_user_by_id(self.user_id)
        if not self.user:
            messagebox.showerror("Erreur", "Utilisateur introuvable.")
            self.go_home(); return

        accounts = self.user.get("accounts", [])
        if not accounts:
            messagebox.showerror("Erreur", "Aucun compte trouvé."); self.go_home(); return

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
        tk.Button(self, text="Disconnect", command=self.go_home).pack(pady=8)

    def go_home(self):
        from gui.homePage import HomeFrame
        self.controller.show_frame(HomeFrame)
    def refresh(self):
        self.controller.load_users()
        u = self.controller.get_user_by_id(self.user_id)
        if u:
            bal = u["accounts"][0].get("balance", 0.0)
            self.balance_label.config(text=f"Balance: {bal:.2f} EUR")

    def open_deposit(self, uid):
        df = self.controller.frames.get(DepositFrame)
        if df:
            df.set_user(uid)
            self.controller.show_frame(DepositFrame)
        else:
            messagebox.showerror("Erreur", "Frame dépôt indisponible.")

    def open_withdraw(self):
        messagebox.showinfo("Info", "Retrait non implémenté (à venir).")

    def open_transfer(self):
        messagebox.showinfo("Info", "Transfert non implémenté (à venir).")