import os
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("WCA ID Card Generator")
        self.geometry("1050x660")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        

        self.leftframe = ctk.CTkFrame(self)
        self.leftframe.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.upload_button = ctk.CTkButton(self.leftframe, text="Upload Photo", command=self.open_image)
        self.upload_button.pack(pady=10)
        
        self.name_entry = ctk.CTkEntry(self.leftframe, placeholder_text="Enter Name")
        self.name_entry.pack(pady=8)
        self.name_entry.bind("<KeyRelease>", self.update_preview)
        
        self.id_entry = ctk.CTkEntry(self.leftframe, placeholder_text="Enter WCA ID")
        self.id_entry.pack(pady=8)
        self.id_entry.bind("<KeyRelease>", self.update_preview)
        
        self.status_entry = ctk.CTkEntry(self.leftframe, placeholder_text="Enter Status")
        self.status_entry.pack(pady=8)
        self.status_entry.bind("<KeyRelease>", self.update_preview)
        
        self.color_entry = ctk.CTkEntry(self.leftframe, placeholder_text="Hex Color (e.g: #RRGGBB)")
        self.color_entry.pack(pady=8)
        self.color_entry.bind("<KeyRelease>", self.update_preview)
        
        self.events_title_lbl = ctk.CTkLabel(self.leftframe, text="Select Participating Events:")
        self.events_title_lbl.pack(anchor="w", padx=20, pady=(10, 5))
        
        self.checkbox_frame = ctk.CTkFrame(self.leftframe, fg_color="transparent")
        self.checkbox_frame.pack(fill="x", padx=20, pady=5)
        
        self.event_3x3 = ctk.StringVar(value="")
        self.event_4x4 = ctk.StringVar(value="")
        self.event_OH = ctk.StringVar(value="")
        self.event_2x2 = ctk.StringVar(value="")
        self.event_5x5 = ctk.StringVar(value="")
        self.event_pyra = ctk.StringVar(value="")
        self.event_bld = ctk.StringVar(value="")
        
        self.check3x3 = ctk.CTkCheckBox(self.checkbox_frame, text="3x3", variable=self.event_3x3, onvalue="3x3", offvalue="", command=self.update_preview)
        self.check3x3.grid(row=0, column=0, padx=15, pady=5, sticky="w")
        
        self.check4x4 = ctk.CTkCheckBox(self.checkbox_frame, text="4x4", variable=self.event_4x4, onvalue="4x4", offvalue="", command=self.update_preview)
        self.check4x4.grid(row=0, column=1, padx=15, pady=5, sticky="w")
        
        self.checkOH = ctk.CTkCheckBox(self.checkbox_frame, text="OH", variable=self.event_OH, onvalue="OH", offvalue="", command=self.update_preview)
        self.checkOH.grid(row=1, column=0, padx=15, pady=5, sticky="w")
        
        self.check2x2 = ctk.CTkCheckBox(self.checkbox_frame, text="2x2", variable=self.event_2x2, onvalue="2x2", offvalue="", command=self.update_preview)
        self.check2x2.grid(row=1, column=1, padx=15, pady=5, sticky="w")
        
        self.check5x5 = ctk.CTkCheckBox(self.checkbox_frame, text="5x5", variable=self.event_5x5, onvalue="5x5", offvalue="", command=self.update_preview)
        self.check5x5.grid(row=2, column=0, padx=15, pady=5, sticky="w")
        
        self.checkpyra = ctk.CTkCheckBox(self.checkbox_frame, text="Pyraminx", variable=self.event_pyra, onvalue="Pyraminx", offvalue="", command=self.update_preview)
        self.checkpyra.grid(row=2, column=1, padx=15, pady=5, sticky="w")
        
        self.checkbld = ctk.CTkCheckBox(self.checkbox_frame, text="3x3 BLD", variable=self.event_bld, onvalue="3x3 BLD", offvalue="", command=self.update_preview)
        self.checkbld.grid(row=3, column=0, padx=15, pady=5, sticky="w")
        
    
        self.rightframe = ctk.CTkFrame(self)
        self.rightframe.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.rightframe.grid_rowconfigure(0, weight=1)
        self.rightframe.grid_rowconfigure(1, weight=1)
        self.rightframe.grid_columnconfigure(0, weight=1)
        
        self.front_frame = ctk.CTkFrame(self.rightframe, fg_color="white", border_width=1, border_color="black")
        self.front_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        self.front_frame.grid_rowconfigure(0, weight=0)
        self.front_frame.grid_rowconfigure(1, weight=1)
        self.front_frame.grid_columnconfigure(0, weight=0)
        self.front_frame.grid_columnconfigure(1, weight=1)
        

        self.front_header = ctk.CTkFrame(self.front_frame, fg_color="blue", corner_radius=0, height=50)
        self.front_header.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.front_header.grid_propagate(False)
        
        self.front_title = ctk.CTkLabel(self.front_header, text="WORLD CUBE ASSOCIATION", font=("Arial", 16, "bold"), text_color="white")
        self.front_title.pack(side="left", padx=15, pady=5)
        
        self.photo_frame = ctk.CTkFrame(self.front_frame, width=130, height=130, border_width=2, border_color="#333333")
        self.photo_frame.grid(row=1, column=0, padx=15, pady=15, sticky="nw")
        self.photo_frame.grid_propagate(False)
        
        self.photo_label = ctk.CTkLabel(self.photo_frame, text="Upload Photo", text_color="#777777")
        self.photo_label.place(relx=0.5, rely=0.5, anchor="center")
        self.photo_frame.bind("<Configure>", self.update_image)
        
        self.info_frame = ctk.CTkFrame(self.front_frame, fg_color="transparent")
        self.info_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        self.name_title = ctk.CTkLabel(self.info_frame, text="Name", font=("Arial", 11), text_color="#999999", anchor="w")
        self.name_title.pack(fill="x", padx=5, pady=(2, 0))
        self.name_label = ctk.CTkLabel(self.info_frame, text="Name", font=("Arial", 14, "bold"), text_color="black", anchor="w")
        self.name_label.pack(fill="x", padx=5, pady=(0, 4))
        
        self.id_title = ctk.CTkLabel(self.info_frame, text="WCA ID", font=("Arial", 11), text_color="#999999", anchor="w")
        self.id_title.pack(fill="x", padx=5, pady=(4, 0))
        self.id_label = ctk.CTkLabel(self.info_frame, text="WCA ID", font=("Arial", 14, "bold"), text_color="black", anchor="w")
        self.id_label.pack(fill="x", padx=5, pady=(0, 10))
        
        self.status_label = ctk.CTkLabel(self.info_frame, text="", font=("Arial", 12, "bold"), text_color="#333333", fg_color="transparent", corner_radius=6, height=30)
        self.status_label.pack(fill="x", padx=5, pady=5)
        
        # ------ BACK BADGE DESIGN ------
        self.back_frame = ctk.CTkFrame(self.rightframe, fg_color="white", border_width=1, border_color="black")
        self.back_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=15)
        self.back_frame.grid_rowconfigure(0, weight=0)
        self.back_frame.grid_rowconfigure(1, weight=1)
        self.back_frame.grid_rowconfigure(2, weight=0)
        self.back_frame.grid_columnconfigure(0, weight=1)
        
        self.back_header = ctk.CTkFrame(self.back_frame, fg_color="blue", corner_radius=0, height=50)
        self.back_header.grid(row=0, column=0, sticky="ew")
        self.back_header.grid_propagate(False)
        
        self.back_title = ctk.CTkLabel(self.back_header, text="WORLD CUBE ASSOCIATION", font=("Arial", 16, "bold"), text_color="white")
        self.back_title.pack(side="left", padx=15, pady=5)
        
        self.back_content = ctk.CTkFrame(self.back_frame, fg_color="transparent")
        self.back_content.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        self.events_header_lbl = ctk.CTkLabel(self.back_content, text="Participating Events", font=("Arial", 13, "bold"), text_color="black", anchor="w")
        self.events_header_lbl.pack(fill="x", pady=(5, 0))
        
        self.line_separator = ctk.CTkFrame(self.back_content, fg_color="#cccccc", height=1)
        self.line_separator.pack(fill="x", pady=(0, 5))
        
        self.events_label = ctk.CTkLabel(self.back_content, text="None Selected", font=("Arial", 12), text_color="black", justify="left", anchor="nw", wraplength=400)
        self.events_label.pack(fill="both", expand=True, pady=5)
         
        self.back_bottom_row = ctk.CTkFrame(self.back_content, fg_color="transparent")
        self.back_bottom_row.pack(fill="x", pady=(10, 5))
        
        self.signature_box = ctk.CTkFrame(self.back_bottom_row, fg_color="white", border_width=1.5, border_color="#0060A9", height=45, corner_radius=6)
        self.signature_box.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.signature_box.pack_propagate(False)
        
        self.signature_title = ctk.CTkLabel(self.signature_box, text="Signature:", font=("Arial", 10), text_color="#0060A9")
        self.signature_title.pack(side="left", padx=10)
        
        self.barcode_container = ctk.CTkFrame(self.back_bottom_row, fg_color="transparent", width=160, height=45)
        self.barcode_container.pack(side="right")
        self.barcode_container.pack_propagate(False)
        
        self.barcode_label = ctk.CTkLabel(
            self.barcode_container, 
            text="||||||||||||||||||", 
            font=("Arial", 32), 
            text_color="black"
        )
        self.barcode_label.place(relx=1.0, rely=0.5, anchor="e")
        
        

    def open_image(self):
        filepath = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.webp")])
        if filepath:
            self.original_image = Image.open(filepath)
            self.update_image()

    def update_image(self, event=None):
        if hasattr(self, "original_image"):
            self.fit_image_to_frame(self.original_image, self.photo_frame, self.photo_label)

    def fit_image_to_frame(self, image, frame, label):
        frame_width = frame.winfo_width()
        frame_height = frame.winfo_height()
        if frame_width <= 1 or frame_height <= 1:
            frame_width, frame_height = 130, 130
            
        img_width, img_height = image.size
        
        min_dim = min(img_width, img_height)
        left = (img_width - min_dim) / 2
        top = (img_height - min_dim) / 2
        right = (img_width + min_dim) / 2
        bottom = (img_height + min_dim) / 2
        cropped_image = image.crop((left, top, right, bottom))
        
        display_size = min(frame_width, frame_height)
        
        resized = cropped_image.resize((display_size, display_size), Image.Resampling.LANCZOS)
        tk_image = ImageTk.PhotoImage(resized)
        
        label.configure(image=tk_image, text="")
        label.image = tk_image

    def update_preview(self, event=None):
        name_txt = self.name_entry.get().strip()
        self.name_label.configure(text=name_txt if name_txt else "Name")
        
        id_txt = self.id_entry.get().strip()
        self.id_label.configure(text=id_txt if id_txt else "WCA ID")
        
        if id_txt:
            simulated_bars = ""
            for char in id_txt.upper():
                simulated_bars += "|||" if ord(char) % 2 == 0 else "||"
            self.barcode_label.configure(text=simulated_bars[:25])
        else:
            self.barcode_label.configure(text="||||||||||||||||||")
        
        status_txt = self.status_entry.get().strip()
        self.status_label.configure(text=status_txt.upper() if status_txt else "")
        
        colour = self.color_entry.get().strip()
        if colour != "" and status_txt != "":
            try:
                self.status_label.configure(fg_color=colour, text_color="white")
            except Exception:
                pass
        else:
            self.status_label.configure(fg_color="transparent", text_color="#333333")
                
        events = []
        if self.event_3x3.get():  events.append(self.event_3x3.get())
        if self.event_4x4.get():  events.append(self.event_4x4.get())
        if self.event_OH.get():   events.append(self.event_OH.get())
        if self.event_2x2.get():  events.append(self.event_2x2.get())
        if self.event_5x5.get():  events.append(self.event_5x5.get())
        if self.event_pyra.get(): events.append(self.event_pyra.get())
        if self.event_bld.get():  events.append(self.event_bld.get())
            
        events_text = ", ".join(events) if events else "None Selected"
        self.events_label.configure(text=events_text)

app = App()
app.mainloop()