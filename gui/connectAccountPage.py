from tkinter import messagebox
import tkinter as tk

from gui.codePage import CodeFrame
from utils.utils import hash_password


class ConnectAccountFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        tk.Label(self, text="Connect Account", font=("Arial", 16)).pack(pady=12)

        tk.Label(self, text="Identifiant (ID numérique):").pack()
        self.entry_id = tk.Entry(self); self.entry_id.pack()
        tk.Label(self, text="Password:").pack()
        self.entry_password = tk.Entry(self, show="*"); self.entry_password.pack()

        tk.Button(self, text="Submit", command=self.submit_connection).pack(pady=10)
        tk.Button(self, text="Back", command= self.go_home).pack()

    def go_home(self):
        from gui.homePage import HomeFrame
        self.controller.show_frame(HomeFrame)

    def submit_connection(self):
        ident = self.entry_id.get().strip()
        raw_pw = self.entry_password.get()
        if not (ident.isdigit() and raw_pw):
            messagebox.showerror("Erreur", "Identifiant numérique et mot de passe requis.")
            return
        uid = int(ident)
        pw = hash_password(raw_pw)
        self.controller.load_users()
        user = self.controller.get_user_by_id(uid)
        if user and user.get("password") == pw:
            code_frame = CodeFrame(self.parent, self.controller, uid)
            code_frame.grid(row=0, column=0, sticky="nsew")
            self.controller.frames[CodeFrame] = code_frame
            self.controller.show_frame(CodeFrame)
            self.entry_id.delete(0, tk.END); self.entry_password.delete(0, tk.END)
            return
        messagebox.showerror("Erreur", "Identifiant ou mot de passe invalide.")
