from tkinter import messagebox
import tkinter as tk



class HomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Bank Home", font=("Arial", 18)).pack(pady=20)
        tk.Button(self, text="Create Account", width=25, command= self.go_to_create_account).pack(pady=8)
        tk.Button(self, text="Connect Account", width=25, command=self.go_to_connect_account).pack(pady=8)
        tk.Button(self, text="Exit", width=25, command=self.controller.destroy).pack(pady=12)

    def go_to_create_account(self):
        from gui.accountCreationPage import CreateAccountFrame
        self.controller.show_frame(CreateAccountFrame)
    
    def go_to_connect_account(self):
        from gui.connectAccountPage import ConnectAccountFrame
        self.controller.show_frame(ConnectAccountFrame)