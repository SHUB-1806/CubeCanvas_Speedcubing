# project.py

import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw
from tkinter import filedialog
import os
import math

class WCAIDGenerator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("WCA ID Card Generator")
        self.geometry("1100x700")
        
        # memory pointers for our image buffers
        self.portrait_img = None
        self.barcode_img = None
        self.logo_img = None 
        self.front_bg_img = None
        self.back_bg_img = None
        self.events_img = None
        
        # set default status color to match the sample
        self.current_status_color = "#27AE60"

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_left_panel()
        self.setup_right_panel()
        
        # init default buffers
        self.generate_silhouette()
        self.generate_barcode()
        self.load_wca_logo()
        self.update_events() # init the event icon buffer

    def setup_left_panel(self):
        self.left_panel = ctk.CTkFrame(self, width=320, corner_radius=0)
        self.left_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.left_panel.grid_propagate(False)

        ctk.CTkLabel(self.left_panel, text="INPUT FORM", font=("Arial", 16, "bold")).pack(pady=(10, 20))

        self.upload_btn = ctk.CTkButton(self.left_panel, text="Upload 1x1 Photo", command=self.load_photo)
        self.upload_btn.pack(pady=10, fill="x", padx=20)

        # entry buffers tied to hardware interrupts
        self.name_entry = ctk.CTkEntry(self.left_panel, placeholder_text="Name (e.g. Max Park)")
        self.name_entry.pack(pady=10, fill="x", padx=20)
        self.name_entry.bind("<KeyRelease>", self.update_name)

        self.wcaid_entry = ctk.CTkEntry(self.left_panel, placeholder_text="WCA ID (e.g. 2012PARK03)")
        self.wcaid_entry.pack(pady=10, fill="x", padx=20)
        self.wcaid_entry.bind("<KeyRelease>", self.update_wcaid)

        self.status_entry = ctk.CTkEntry(self.left_panel, placeholder_text="Status (e.g. MEMBER)")
        self.status_entry.pack(pady=10, fill="x", padx=20)
        self.status_entry.bind("<KeyRelease>", self.update_status)

        self.color_entry = ctk.CTkEntry(self.left_panel, placeholder_text="Status Hex (e.g. #27AE60)")
        self.color_entry.pack(pady=10, fill="x", padx=20)
        self.color_entry.bind("<KeyRelease>", self.update_color)

        ctk.CTkLabel(self.left_panel, text="Participating Events:").pack(pady=(20, 5), anchor="w", padx=20)
        
        self.events = ["3x3", "OH", "4x4", "Blind", "Megaminx"]
        self.checkboxes = []
        for event in self.events:
            cb = ctk.CTkCheckBox(self.left_panel, text=event, command=self.update_events)
            cb.pack(pady=5, anchor="w", padx=20)
            self.checkboxes.append(cb)

    def load_wca_logo(self):
        logo_path = "wca_logo.png"
        if os.path.exists(logo_path):
            img = Image.open(logo_path).convert("RGBA").resize((70, 70), Image.Resampling.LANCZOS)
        else:
            # fallback dummy block if file is missing
            img = Image.new('RGBA', (70, 70), (0,0,0,0))
            draw = ImageDraw.Draw(img)
            draw.ellipse((5, 5, 65, 65), fill="#0044BB", outline="white", width=2)
            draw.text((25, 25), "WCA", fill="white")
            
        self.logo_img = ctk.CTkImage(light_image=img, size=(70, 70))
        # force the label to use the alpha channel mask
        self.front_logo_label.configure(image=self.logo_img, fg_color="transparent")
        self.back_logo_label.configure(image=self.logo_img, fg_color="transparent")

    def draw_wca_background(self):
        # manually allocate the complex geometric pattern
        img = Image.new('RGBA', (800, 500), '#FFFFFF')
        draw = ImageDraw.Draw(img)
        
        draw.polygon([(0,0), (250,0), (125, 200), (0, 200)], fill="#203E79", outline="white", width=4) 
        draw.polygon([(250,0), (550,0), (400, 200), (125, 200)], fill="#DF2B21", outline="white", width=4) 
        draw.polygon([(550,0), (800,0), (800, 200), (400, 200)], fill="#27AE60", outline="white", width=4) 
        draw.polygon([(0,200), (125, 200), (250, 400), (0, 400)], fill="#F39C12", outline="white", width=4) 
        draw.polygon([(125,200), (400, 200), (250, 400)], fill="#F1C40F", outline="white", width=4) 
        draw.polygon([(400,200), (800, 200), (800, 400), (250, 400)], fill="#2980B9", outline="white", width=4) 
        
        return img

    def draw_back_background(self):
        img = Image.new('RGBA', (800, 500), '#F5F5F5')
        draw = ImageDraw.Draw(img)
        # draw magnetic stripe
        draw.rectangle([0, 50, 800, 130], fill="#111111")
        # draw signature box background
        draw.rectangle([40, 250, 400, 320], fill="white", outline="#AAAAAA", width=2)
        return img

    def generate_events_buffer(self, active_events):
        # custom rasterizer to build the official wca icons geometrically
        img = Image.new('RGBA', (400, 50), (0,0,0,0))
        draw = ImageDraw.Draw(img)
        
        x_offset = 0
        for ev in active_events:
            if ev == "3x3":
                for row in range(3):
                    for col in range(3):
                        draw.rectangle([x_offset + col*8, 10 + row*8, x_offset + col*8 + 6, 10 + row*8 + 6], fill="black")
            elif ev == "4x4":
                for row in range(4):
                    for col in range(4):
                        draw.rectangle([x_offset + col*6, 10 + row*6, x_offset + col*6 + 4, 10 + row*6 + 4], fill="black")
            elif ev == "OH":
                for row in range(3):
                    for col in range(3):
                        draw.rectangle([x_offset + col*6, 15 + row*6, x_offset + col*6 + 4, 15 + row*6 + 4], fill="black")
                draw.text((x_offset + 20, 18), "OH", fill="black")
            elif ev == "Blind":
                for row in range(3):
                    for col in range(3):
                        draw.rectangle([x_offset + col*8, 10 + row*8, x_offset + col*8 + 6, 10 + row*8 + 6], fill="black")
                draw.rectangle([x_offset - 2, 17, x_offset + 26, 23], fill="black") # blindfold strip
            elif ev == "Megaminx":
                # calculate simple pentagon vectors
                cx, cy, r = x_offset + 12, 22, 12
                pts = [(cx + r*math.sin(i*2*math.pi/5), cy - r*math.cos(i*2*math.pi/5)) for i in range(5)]
                draw.polygon(pts, outline="black", width=2)
                
            x_offset += 45
            
        return img

    def setup_right_panel(self):
        self.right_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # FRONT CARD LAYOUT 
        self.front_card = ctk.CTkFrame(self.right_panel, corner_radius=15, border_width=3, border_color="#333333")
        self.front_card.pack(pady=10, expand=True, fill="both")
        
        self.front_bg_img = ctk.CTkImage(light_image=self.draw_wca_background(), size=(800, 500))
        self.front_bg_label = ctk.CTkLabel(self.front_card, text="", image=self.front_bg_img)
        self.front_bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.header_banner = ctk.CTkLabel(self.front_card, text=" WORLD CUBE ASSOCIATION ", font=("Arial", 14, "bold"), fg_color="white", text_color="black", corner_radius=2)
        self.header_banner.place(relx=0.05, rely=0.1, anchor="nw")

        # Top Right Logo with forced alpha
        self.front_logo_label = ctk.CTkLabel(self.front_card, text="", fg_color="transparent")
        self.front_logo_label.place(relx=0.95, rely=0.05, anchor="ne")

        self.info_frame = ctk.CTkFrame(self.front_card, fg_color="#D1DDF0", corner_radius=5)
        self.info_frame.place(relx=0.05, rely=0.85, anchor="sw")
        
        self.name_label = ctk.CTkLabel(self.info_frame, text="Name", font=("Arial", 28, "bold"), text_color="black")
        self.name_label.pack(anchor="w", padx=15, pady=(10, 0))
        
        self.wcaid_label = ctk.CTkLabel(self.info_frame, text="WCA ID", font=("Arial", 18), text_color="#333333")
        self.wcaid_label.pack(anchor="w", padx=15, pady=(0, 10))

        self.status_box = ctk.CTkFrame(self.front_card, fg_color=self.current_status_color, corner_radius=8)
        self.status_box.place(relx=0.85, rely=0.85, anchor="se")
        
        self.portrait_label = ctk.CTkLabel(self.status_box, text="")
        self.portrait_label.pack(padx=5, pady=(5, 0))
        
        self.status_label = ctk.CTkLabel(self.status_box, text="MEMBER", font=("Arial", 14, "bold"), text_color="white")
        self.status_label.pack(pady=4)

        # BACK CARD LAYOUT
        self.back_card = ctk.CTkFrame(self.right_panel, corner_radius=15, border_width=3, border_color="#333333")
        self.back_card.pack(pady=10, expand=True, fill="both")
        
        self.back_bg_img = ctk.CTkImage(light_image=self.draw_back_background(), size=(800, 500))
        self.back_bg_label = ctk.CTkLabel(self.back_card, text="", image=self.back_bg_img)
        self.back_bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Static text header for events
        self.events_text = ctk.CTkLabel(self.back_card, text="Participating events:", font=("Arial", 16, "bold"), text_color="black", fg_color="#FFFFFF")
        self.events_text.place(relx=0.05, rely=0.32, anchor="w")

        # Dynamic rasterized icon layer
        self.events_icons_label = ctk.CTkLabel(self.back_card, text="", fg_color="#FFFFFF")
        self.events_icons_label.place(relx=0.05, rely=0.45, anchor="w")

        self.barcode_label = ctk.CTkLabel(self.back_card, text="", fg_color="transparent")
        self.barcode_label.place(relx=0.05, rely=0.9, anchor="sw")

        self.back_logo_label = ctk.CTkLabel(self.back_card, text="", fg_color="transparent")
        self.back_logo_label.place(relx=0.95, rely=0.95, anchor="se")
        
        self.right_panel.bind("<Configure>", self.handle_resize)

    # INTERRUPT HANDLERS 

    def update_name(self, event):
        self.name_label.configure(text=self.name_entry.get() or "Max Park")

    def update_wcaid(self, event):
        val = self.wcaid_entry.get() or "2012PARK03"
        self.wcaid_label.configure(text=val)
        self.generate_barcode(val) 

    def update_status(self, event):
        self.status_label.configure(text=self.status_entry.get() or "MEMBER")

    def update_color(self, event):
        hex_val = self.color_entry.get()
        try:
            # tkinter uses american spelling internally
            if len(hex_val) == 7 and hex_val.startswith("#"):
                self.current_status_color = hex_val
                self.status_box.configure(fg_color=hex_val)
        except Exception:
            pass 

    def update_events(self):
        active = [cb.cget("text") for cb in self.checkboxes if cb.get() == 1]
        
        # pass the active pointers to the icon rasterizer
        icon_buffer = self.generate_events_buffer(active)
        self.events_img = ctk.CTkImage(light_image=icon_buffer, size=(400, 50))
        self.events_icons_label.configure(image=self.events_img)

    def handle_resize(self, event):
        # dynamic re-allocation of background buffers to prevent pixelation
        if event.width > 50 and event.height > 50:
            target_w = event.width
            target_h = int(event.height / 2) - 20 
            
            self.front_bg_img.configure(size=(target_w, target_h))
            self.back_bg_img.configure(size=(target_w, target_h))

    # MEMORY/BUFFER MANIPULATION

    def load_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if file_path:
            img = Image.open(file_path).resize((130, 150), Image.Resampling.LANCZOS)
            self.portrait_img = ctk.CTkImage(light_image=img, size=(130, 150))
            self.portrait_label.configure(image=self.portrait_img)

    def generate_silhouette(self):
        img = Image.new('RGB', (130, 150), color='#F2F2F2')
        draw = ImageDraw.Draw(img)
        draw.ellipse((35, 20, 95, 80), fill="#CCCCCC") 
        draw.ellipse((10, 85, 120, 200), fill="#CCCCCC") 
        
        self.portrait_img = ctk.CTkImage(light_image=img, size=(130, 150))
        self.portrait_label.configure(image=self.portrait_img)

    def generate_barcode(self, text="2012PARK03"):
        img = Image.new('RGB', (250, 60), color='white')
        draw = ImageDraw.Draw(img)
        
        seed = sum(ord(c) for c in text)
        x = 5
        for i in range(50):
            width = (seed + i) % 4 + 1
            if i % 2 == 0:
                draw.rectangle([x, 0, x+width, 60], fill="black")
            x += width
            if x > 240: break
            
        self.barcode_img = ctk.CTkImage(light_image=img, size=(250, 60))
        self.barcode_label.configure(image=self.barcode_img)

if __name__ == "__main__":
    app = WCAIDGenerator()
    app.mainloop()