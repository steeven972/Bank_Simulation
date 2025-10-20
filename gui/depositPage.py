import tkinter as tk
from tkinter import messagebox
import datetime




class DepositFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
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
        from gui.accountInterfacePage import AccountInterface
        acc = AccountInterface(self.controller, self.user_id)
        acc.grid(row=0, column=0, sticky="nsew")
        self.controller.frames[AccountInterface] = acc
        self.controller.show_frame(AccountInterface)

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
        self.controller.load_users()
        updated = False
        for u in self.controller.users:
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

        self.controller.save_users()
        self.entry_amount.delete(0, tk.END)
        messagebox.showinfo("Succès", f"Dépôt de {amount:.2f} EUR effectué.\nNouveau solde : {new_balance:.2f} EUR")

        self.display_account_interface_refreshed()
        # recreate AccountInterface to refresh display
    def display_account_interface_refreshed(self):
        from gui.accountInterfacePage import AccountInterface
        acc_frame = AccountInterface(self.parent, self.controller, self.user_id)
        acc_frame.grid(row=0, column=0, sticky="nsew")
        self.controller.frames[AccountInterface] = acc_frame
        self.controller.show_frame(AccountInterface)
