import customtkinter as ctk
from tkinter import filedialog

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.photo_path = None

        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            self,
            text="Input Panel",
            font=("Helvetica", 22, "bold")
        )

        title.pack(pady=20)

        self.upload_button = ctk.CTkButton(
            self,
            text="Upload 1x1 Photo",
            command=self.upload_photo
        )

        self.upload_button.pack(fill="x", padx=20, pady=10)

        self.name_label = ctk.CTkLabel(
            self,
            text="Name"
        )

        self.name_label.pack(anchor="w", padx=20)

        self.name_entry = ctk.CTkEntry(self)

        self.name_entry.pack(fill="x", padx=20, pady=5)

        self.id_label = ctk.CTkLabel(
            self,
            text="WCA ID"
        )

        self.id_label.pack(anchor="w", padx=20)

        self.id_entry = ctk.CTkEntry(self)

        self.id_entry.pack(fill="x", padx=20, pady=5)

        self.status_label = ctk.CTkLabel(
            self,
            text="Status"
        )

        self.status_label.pack(anchor="w", padx=20)

        self.status_entry = ctk.CTkEntry(self)

        self.status_entry.pack(fill="x", padx=20, pady=5)

        self.color_label = ctk.CTkLabel(
            self,
            text="Status Colour (#RRGGBB)"
        )

        self.color_label.pack(anchor="w", padx=20)

        self.color_entry = ctk.CTkEntry(self)

        self.color_entry.insert(0, "#00AA55")

        self.color_entry.pack(fill="x", padx=20, pady=5)

        values = [
            "2x2",
            "3x3",
            "4x4",
            "5x5",
            "6x6",
            "Megaminx",
            "Square-1",
            "Clock",
            "3BLD",
            "4BLD",
            "5BLD",
            "MBLD",
            "OH",
            "Pyraminx",
            "Skewb",
            "FMC"
        ]

        self.scrollable_checkbox_frame = self.ScrollableCheckboxFrame(self, title="Participating Events", values=values)
        self.scrollable_checkbox_frame.pack(fill='both', expand=True, padx = 20, pady = 20)

        self.save_button = ctk.CTkButton(
            self,
            text="Save ID",
            command=self.controller.save_cards
        )

        self.save_button.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.name_entry.bind("<KeyRelease>", self.update_preview)
        self.id_entry.bind("<KeyRelease>", self.update_preview)
        self.status_entry.bind("<KeyRelease>", self.update_preview)
        self.color_entry.bind("<KeyRelease>", self.update_preview)

    def upload_photo(self):
        filename = filedialog.askopenfilename(
            title="Select Portrait",
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg")
            ]
        )

        if filename:
            self.photo_path = filename
            self.controller.update_preview()

    def get_data(self):

        selected_events = self.scrollable_checkbox_frame.get()

        return {
            "photo": self.photo_path,
            "name": self.name_entry.get(),
            "wca_id": self.id_entry.get(),
            "status": self.status_entry.get(),
            "colour": self.color_entry.get(),
            "events": selected_events
        }

    def update_preview(self, event=None):
        self.controller.update_preview()

    class ScrollableCheckboxFrame(ctk.CTkScrollableFrame):
        def __init__(self, master, title, values):
            super().__init__(master, label_text=title)
            self.grid_columnconfigure(0, weight=1)
            self.values = values
            self.checkboxes = []

            for i, value in enumerate(self.values):
                checkbox = ctk.CTkCheckBox(self, text=value, command=master.update_preview)
                checkbox.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
                self.checkboxes.append(checkbox)

        def get(self):
            checked_checkboxes = []
            for checkbox in self.checkboxes:
                if checkbox.get() == 1:
                    checked_checkboxes.append(checkbox.cget("text"))
            return checked_checkboxes