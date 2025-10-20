import tkinter as tk
import tkinter.messagebox as messagebox
import hashlib
import json
import os
import random
import datetime

from backend.account import BankAccount
from backend.user import User

from gui.homePage import HomeFrame
from gui.accountCreationPage import CreateAccountFrame
from gui.connectAccountPage import ConnectAccountFrame
from gui.codePage import CodeFrame
from gui.accountInterfacePage import AccountInterface
from gui.depositPage import DepositFrame


from utils.utils import generate_iban, USERS_FILE, ensure_users_file, hash_password

class Interface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bank Application")
        self.geometry("460x420")

        ensure_users_file()
        self.users = []
        self.load_users()

        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        
        self.frames = {}
        for F in (HomeFrame, CreateAccountFrame, ConnectAccountFrame, DepositFrame):
            frame = F(container, self)
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


if __name__ == "__main__":
    ensure_users_file()
    app = Interface()
    app.mainloop()
