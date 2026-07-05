import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageColor
import os

class Preview(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.CARD_WIDTH = 450
        self.CARD_HEIGHT = 260

        self.front_image = None
        self.back_image = None

        self.front_photo = None
        self.back_photo = None

        self.placeholder_image = Image.open("assets/placeholder.png")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.grid_columnconfigure(0, weight=1)

        self.front_frame = ctk.CTkFrame(self, corner_radius=15)

        self.front_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=15,
            pady=(15,8)
        )

        self.front_frame.grid_rowconfigure(0, weight=1)
        self.front_frame.grid_columnconfigure(0, weight=1)

        self.front_label = ctk.CTkLabel(
            self.front_frame,
            text=""
        )

        self.front_label.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        self.back_frame = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        self.back_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=15,
            pady=(8, 15)
        )

        self.back_frame.grid_rowconfigure(
            0,
            weight=1
        )

        self.back_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.back_label = ctk.CTkLabel(
            self.back_frame,
            text=""
        )

        self.back_label.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        self.front_frame.bind(
            "<Configure>",
            self.on_resize
        )

        self.back_frame.bind(
            "<Configure>",
            self.on_resize
        )

        self.update_card(
            {
                "photo": None,
                "name": "",
                "wca_id": "",
                "status": "",
                "colour": "#008844",
                "events": []
            }
        )

    def on_resize(self, event=None):
        self.display_cards()

    def update_card(self, data):
        self.front_image = self.draw_front_card(data)
        self.back_image = self.draw_back_card(data)
        self.display_cards()

    def display_cards(self):
        if self.front_image is not None:
            width = max(self.front_frame.winfo_width() - 20,100)
            height = max(self.front_frame.winfo_height() - 20,100)

            image = self.front_image.copy()

            image.thumbnail(
                (width, height),
                Image.Resampling.LANCZOS
            )

            self.front_photo = ImageTk.PhotoImage(image)

            self.front_label.configure(image=self.front_photo)

            self.front_label.image = self.front_photo

        if self.back_image is not None:
            width = max(self.back_frame.winfo_width() - 20,100)
            height = max(self.back_frame.winfo_height() - 20,100)

            image = self.back_image.copy()

            image.thumbnail(
                (width, height),
                Image.Resampling.LANCZOS
            )

            self.back_photo = ImageTk.PhotoImage(image)

            self.back_label.configure(image=self.back_photo)

            self.back_label.image = self.back_photo

    def draw_front_card(self, data):
        card = Image.new(
            "RGB",
            (self.CARD_WIDTH, self.CARD_HEIGHT),
            "white"
        )

        draw = ImageDraw.Draw(card)

        try:
            title_font = ImageFont.truetype("arial.ttf", 22)
            heading_font = ImageFont.truetype("arial.ttf", 18)
            text_font = ImageFont.truetype("arial.ttf", 16)
            status_font = ImageFont.truetype("arialbd.ttf", 16)
        except:
            title_font = ImageFont.load_default()
            heading_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            status_font = ImageFont.load_default()

        draw.rectangle(
            [(0, 0), (self.CARD_WIDTH, 45)],
            fill="#0056A3"
        )

        draw.text(
            (15, 10),
            "WORLD CUBE ASSOCIATION",
            fill="white",
            font=title_font
        )

        if os.path.exists("assets/wca_logo.png"):
            logo = Image.open("assets/wca_logo.png").convert("RGBA")
            logo.thumbnail((35, 35), Image.Resampling.LANCZOS)

            card.paste(logo, (400, 5), logo)

        photo = self.placeholder_image

        if data["photo"]:
            if os.path.exists(data["photo"]):
                try:
                    photo = Image.open(data["photo"])
                except:
                    pass

        if photo is not None:
            image = photo.copy()

            image.thumbnail(
                (120, 140),
                Image.Resampling.LANCZOS
            )

            x = 20 + (120 - image.width) // 2
            y = 65 + (140 - image.height) // 2

            card.paste(image, (x, y))

            draw.rectangle(
                [(20, 65), (140, 205)],
                outline="black",
                width=2
            )

        name = data["name"].strip()

        if name == "":
            name = "Name"

        wca_id = data["wca_id"].strip()

        if wca_id == "":
            wca_id = "WCA ID"

        status = data["status"].strip()

        if status == "":
            status = "MEMBER"

        draw.text(
            (170, 75),
            "Name",
            fill="gray",
            font=text_font
        )

        draw.text(
            (170, 95),
            name,
            fill="black",
            font=heading_font
        )

        draw.text(
            (170, 130),
            "WCA ID",
            fill="gray",
            font=text_font
        )

        draw.text(
            (170, 150),
            wca_id,
            fill="black",
            font=heading_font
        )

        colour = data["colour"]

        try:
            ImageColor.getrgb(colour)
        except:
            colour = "#008844"

        draw.rounded_rectangle(
            [(170, 190), (410, 225)],
            radius=8,
            fill=colour
        )

        draw.text(
            (185, 198),
            status,
            fill="white",
            font=status_font
        )

        draw.rectangle(
            [(0, 0), (self.CARD_WIDTH - 1, self.CARD_HEIGHT - 1)],
            outline="black",
            width=2
        )

        return card

    def draw_back_card(self, data):

        card = Image.new(
            "RGB",
            (self.CARD_WIDTH, self.CARD_HEIGHT),
            "white"
        )

        draw = ImageDraw.Draw(card)

        try:
            title_font = ImageFont.truetype("arial.ttf", 22)
            heading_font = ImageFont.truetype("arial.ttf", 18)
            text_font = ImageFont.truetype("arial.ttf", 16)
            footer_font = ImageFont.truetype("arial.ttf", 12)
        except:

            title_font = ImageFont.load_default()
            heading_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            footer_font = ImageFont.load_default()

        draw.rectangle(
            [(0, 0), (self.CARD_WIDTH, 45)],
            fill="#0056A3"
        )

        draw.text(
            (15, 10),
            "WORLD CUBE ASSOCIATION",
            fill="white",
            font=title_font
        )

        if os.path.exists("assets/wca_logo.png"):
            logo = Image.open("assets/wca_logo.png").convert("RGBA")
            logo.thumbnail((35, 35), Image.Resampling.LANCZOS)

            card.paste(logo, (400, 5), logo)

        draw.text(
            (20, 65),
            "Participating Events",
            fill="black",
            font=heading_font
        )

        draw.line(
            [(20, 95), (430, 95)],
            fill="gray",
            width=2
        )

        events = data.get("events", [])

        x = 30
        y = 100

        max_width = 400
        spacing = 10

        for event in events:

            text = f"\N{BULLET} {event}"

            bbox = draw.textbbox((0, 0), text, font=text_font)
            text_width = bbox[2] - bbox[0]

            if x + text_width > max_width:
                x = 30
                y += 30

            draw.text((x, y), text, fill="black", font=text_font)

            x += text_width + spacing

        draw.rounded_rectangle(
            [(20, 185), (430, 225)],
            radius=10,
            outline="#0056A3",
            width=2
        )

        draw.text(
            (35, 197),
            "Signature: ",
            fill="#0056A3",
            font=footer_font
        )

        draw.text(
            (20, 238),
            "www.worldcubeassociation.org",
            fill="gray",
            font=footer_font
        )

        draw.rectangle(
            [(0, 0), (self.CARD_WIDTH - 1, self.CARD_HEIGHT - 1)],
            outline="black",
            width=2
        )

        return card

    def save_cards(self):

        os.makedirs("generated", exist_ok=True)

        if self.front_image:
            self.front_image.save("generated/front.png")

        if self.back_image:
            self.back_image.save("generated/back.png")