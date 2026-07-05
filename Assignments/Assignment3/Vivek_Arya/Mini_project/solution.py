import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("WCA ID Card Generator")
        self.geometry("1000x600")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
    #Left frame
        self.leftframe = ctk.CTkFrame(self)
        self.leftframe.grid(row=0,column=0,sticky="nsew",padx=10,pady=10)
    #Right frame
        self.rightframe = ctk.CTkFrame(self)
        self.rightframe.grid(row=0,column=1,sticky="nsew",padx=10, pady=10)
        self.rightframe.grid_rowconfigure(0, weight=1)
        self.rightframe.grid_rowconfigure(1, weight=1)
        self.rightframe.grid_columnconfigure(0, weight=1)

    #front frame
        self.front_frame = ctk.CTkFrame(self.rightframe)
        self.front_frame.grid(row=0,column=0,sticky="nsew",padx=10,pady=10)
        self.front_frame.grid_rowconfigure(0, weight=0)   
        self.front_frame.grid_rowconfigure(1, weight=3)   
        self.front_frame.grid_rowconfigure(2, weight=1) 
        self.front_title = ctk.CTkLabel(self.front_frame,text="WORLD CUBE ASSOCIATION",font=("Arial",18,"bold"))
        self.front_frame.grid_columnconfigure(0, weight=0)
        self.front_frame.grid_columnconfigure(1, weight=0)
        self.front_title.grid(row=0, column=0, columnspan=2, pady=10)
        self.front_frame.grid_columnconfigure(2, weight=1)

    #photo frame
        self.photo_frame = ctk.CTkFrame(self.front_frame,width = 170,height = 220,border_width=2)
        self.photo_frame.grid(row=1,column=0,padx=(40,5),pady=20,sticky="e")
        self.photo_frame.grid_propagate(False)
        self.photo_label = ctk.CTkLabel(self.photo_frame,text="Upload Photo")
        self.photo_label.place(relx=0.5,rely=0.5,anchor="center")
        self.photo_frame.bind("<Configure>", self.update_image)
         
        self.info_frame = ctk.CTkFrame(self.front_frame,width=260,height=250)
        self.info_frame.grid_propagate(False)
        self.info_frame.grid(row=1,column=1,padx=(5,40),pady=20,sticky="w")
        self.info_frame.grid_rowconfigure(0, weight=1)
        self.info_frame.grid_rowconfigure(1, weight=1)
        self.info_frame.grid_rowconfigure(2, weight=1)
        self.info_frame.grid_columnconfigure(0, weight=1)
        
        self.name_label = ctk.CTkLabel(self.info_frame,text="Name",font=("Arial",18,))
        self.name_label.pack(anchor="w", padx=20, pady=(30,25))
    
        
        self.id_label = ctk.CTkLabel(self.info_frame,text="WCA ID",font=("Arial",15))
        self.id_label.pack(anchor="w", padx=20, pady=(0,25))

        self.status_label = ctk.CTkLabel(self.info_frame,text="Status",fg_color="gray25",corner_radius=10,width=150,
        height=35,font=("Arial",15,))
        self.status_label.pack(anchor="w", padx=20)
 
    
    #Back Frame
        self.back_frame = ctk.CTkFrame(self.rightframe)
        self.back_frame.grid(row=1,column=0,sticky="nsew",padx=10,pady=10)
        self.back_title = ctk.CTkLabel(self.back_frame,text="BACK ID CARD",font=("Arial",18,"bold"))
        self.back_title.grid(row=0,column=0,columnspan=2,pady=10)
        self.back_frame.grid_columnconfigure(0, weight=2)
        self.back_frame.grid_columnconfigure(1, weight=1)
        self.events_label = ctk.CTkLabel(self.back_frame,text="Participating Events")
        self.events_label.grid(row=1,column=0,sticky="nw",padx=20,pady=20)

        self.barcode_label = ctk.CTkLabel(self.back_frame,text="""▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌▌""",font=("Consolas",15))
        self.barcode_label.grid(row=1,column=1,padx=20,pady=20)
    #Widgets
        self.upload_button = ctk.CTkButton(self.leftframe,text="Upload Photo",command=self.open_image)
        self.upload_button.pack(pady=10)

        self.name_entry = ctk.CTkEntry(self.leftframe,placeholder_text="Enter Name")
        self.name_entry.pack(pady=10)
        self.name_entry.bind("<KeyRelease>",self.update_preview)

        self.id_entry = ctk.CTkEntry(self.leftframe,placeholder_text="Enter WCA ID")
        self.id_entry.pack(pady=10)
        self.id_entry.bind("<KeyRelease>",self.update_preview)

        self.status_entry = ctk.CTkEntry(self.leftframe, placeholder_text="Enter Status")
        self.status_entry.pack(pady=10)
        self.status_entry.bind("<KeyRelease>",self.update_preview)

        self.color_entry = ctk.CTkEntry(self.leftframe,placeholder_text="Hex Color")
        self.color_entry.pack(pady=10)
        self.color_entry.bind("<KeyRelease>",self.update_preview)
    # checkboxs
        self.event_3x3 = ctk.StringVar(value="")
        self.event_4x4 = ctk.StringVar(value="")
        self.event_OH = ctk.StringVar(value="")

        self.check3x3 = ctk.CTkCheckBox(self.leftframe, text="3x3",variable=self.event_3x3,onvalue="3x3", offvalue="",
        command=self.update_preview)
        self.check3x3.pack(anchor="w", padx=20)

        self.check4x4 = ctk.CTkCheckBox(self.leftframe,text="4x4",variable=self.event_4x4,onvalue="4x4",offvalue="",
        command=self.update_preview)
        self.check4x4.pack(anchor="w", padx=20)

        self.checkOH = ctk.CTkCheckBox(self.leftframe,text="OH",variable=self.event_OH,onvalue="OH",offvalue="",
        command=self.update_preview)
        self.checkOH.pack(anchor="w", padx=20)

    def open_image(self):
        filepath = filedialog.askopenfilename()
        if not filepath:
            return
    
        self.original_image = Image.open(filepath)
        self.update_image()

    def update_image(self, event=None):
        if not hasattr(self, "original_image"):
            return
        self.fit_image_to_frame(
            self.original_image,
            self.photo_frame,
            self.photo_label
        )
    def fit_image_to_frame(self, image, frame, label):
        frame_width = frame.winfo_width()
        frame_height = frame.winfo_height()
        if frame_width <= 1 or frame_height <= 1:
            return

        img_width, img_height = image.size
        scale = min( frame_width / img_width,frame_height / img_height)

        new_width = int(img_width * scale)
        new_height = int(img_height * scale)

        resized = image.resize( (new_width, new_height), Image.Resampling.LANCZOS)

        tk_image = ImageTk.PhotoImage(resized)
        label.configure(image=tk_image,text="")
        label.image = tk_image

    def update_preview(self, event=None):
        self.name_label.configure(text=f"Name : {self.name_entry.get()}")
        self.id_label.configure(text=f"WCA ID : {self.id_entry.get()}")
        self.status_label.configure(text=self.status_entry.get().upper())
        
        colour = self.color_entry.get()
        if colour != "":
            try:
                self.status_label.configure(fg_color=colour)

            except:
                pass
        events = []
        if self.event_3x3.get():
            events.append(self.event_3x3.get())
        if self.event_4x4.get():
            events.append(self.event_4x4.get())
        if self.event_OH.get():
            events.append(self.event_OH.get())
        self.events_label.configure(text="Participating Events\n\n" + ", ".join(events))
        
app=App()
app.mainloop()