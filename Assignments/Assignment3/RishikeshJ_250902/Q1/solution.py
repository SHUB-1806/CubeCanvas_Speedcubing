'''
1. The weight parameter is used to tell how to distribute extra space to rows and columns when a window is resized.
2. This argument is used to stretch the widget to completely filling the assigned grid by sticking to the North, South, East and West edges of the cell, so that when the window resizes the widget expands and contracts alongside the cell.
3. Stacking refers to the order in which widgets are placed on top of each other such that the topmost widget is visible. tkraise() works by bringing the widget called to the top and hence makes it visible.
'''

import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Question 1")
        self.geometry("1000x600")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        frame1 = ctk.CTkFrame(self, fg_color = "red")
        frame2 = ctk.CTkFrame(self, fg_color = "blue")
        frame3 = ctk.CTkFrame(self, fg_color = "green")
        frame4 = ctk.CTkFrame(self, fg_color = "yellow")

        frame1.grid(row=0, column=0, sticky="nsew")
        frame2.grid(row=0, column=1, sticky="nsew")
        frame3.grid(row=1, column=0, sticky="nsew")
        frame4.grid(row=1, column=1, sticky="nsew")

app = App()

app.mainloop()
