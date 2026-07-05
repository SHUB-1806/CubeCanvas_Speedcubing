import customtkinter as ctk

from sidebar import Sidebar
from preview import Preview

class WCA_ID(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Interactive WCA ID Card Generator")
        self.geometry("1200x700")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        self.grid_rowconfigure(0, weight=1)

        self.preview = Preview(self)

        self.preview.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=10,
            pady=10
        )

        self.sidebar = Sidebar(self,controller = self)

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

    def update_preview(self):
        data = self.sidebar.get_data()
        self.preview.update_card(data)

    def save_cards(self):
        self.preview.save_cards()