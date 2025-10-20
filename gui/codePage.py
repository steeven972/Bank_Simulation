from tkinter import messagebox
import tkinter as tk

from gui.accountInterfacePage import AccountInterface



class CodeFrame(tk.Frame):
    def __init__(self, parent, controller, user_id):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
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

        tk.Button(self, text="Back", command=self.go_to_connect_page).pack(pady=8)

    def go_to_connect_page(self):
        from gui.connectAccountPage import ConnectAccountFrame
        self.controller.show_frame(ConnectAccountFrame)

    def add_digit(self, d): self.display.insert(tk.END, d)
    def clear_display(self): self.display.delete(0, tk.END)

    def validate_input(self):
        code_value = self.display.get().strip()
        if not code_value:
            messagebox.showerror("Erreur", "Entrez le code.")
            return
        self.controller.load_users()
        user = self.controller.get_user_by_id(self.user_id)
        if user and str(user.get("code")) == code_value:
            account_frame = AccountInterface(self.parent, self.controller, self.user_id)
            account_frame.grid(row=0, column=0, sticky="nsew")
            self.controller.frames[AccountInterface] = account_frame
            self.controller.show_frame(AccountInterface)
            self.clear_display()
            return
        messagebox.showerror("Erreur", "Code invalide.")
        self.clear_display()
