import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("WCA ID Card Generator")
app.geometry("1200*700")
app.minsize(1000, 600)

app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=2)
app.grid_rowconfigure(0, weight=1)

left_frame = ctk.CTkFrame(app)
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

right_frame = ctk.CTkFrame(app)
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

right_frame.grid_columnconfigure(0, weight=1)
right_frame.grid_columnconfigure(1, weight=1)

ctk.CTkLabel(left_frame, text="Name").pack(pady=(20,5))
name_entry = ctk.CTkEntry(left_frame, width=250)
name_entry.pack()

ctk.CTkLabel(left_frame, text="WCA ID").pack(pady=(15,5))
id_entry = ctk.CTkEntry(left_frame, width=250)
id_entry.pack()

ctk.CTkLabel(left_frame, text="Status").pack(pady=(15,5))
status_entry = ctk.CTkEntry(left_frame, width=250)
status_entry.pack()

ctk.CTkLabel(left_frame, text="Status Color(Hex)").pack(pady=(15,5))
color_entry = ctk.CTkEntry(left_frame, width=250)
color_entry.insert(0, "#00AA00")
color_entry.pack()

photo_path = None

def upload_photo():
    global photo_path
    filename = filedialog.askopenfilename(filetypes=[("Image Files","*.png *.jpg *.jpeg"),
                                                     ("All Files","*.*")])
    print(filename)

    if filename:
        photo_path = filename
        update_preview()

upload_btn = ctk.CTkButton(
    left_frame,
    text="Upload 1*1 Photo",
    command=upload_photo
)   
upload_btn.pack(pady=20)

preview_frame = ctk.CTkFrame(right_frame)
preview_frame.pack(fill="both", expand=True, padx=10, pady=10)

ctk.CTkLabel(preview_frame, text="Front ID Preview",
             font=("Arial", 18, "bold")).grid(row=0, column=0,pady=10)

front_canvas = ctk.CTkCanvas(
    preview_frame, width=350, height=220, bg="white"
)
front_canvas.grid(row=1, column=0, padx=10, pady=10)

ctk.CTkLabel(preview_frame, text="Back ID Preview",
             font=("Arial", 18, "bold")).grid(row=0, column=1,pady=10)

back_canvas = ctk.CTkCanvas(
    preview_frame, width=350, height=220, bg="white"
)
back_canvas.grid(row=1, column=1, padx=10, pady=10)

def draw_front():
    front_canvas.delete("all")

    front_canvas.create_rectangle(10, 10, 340, 210, fill="lightblue", outline="black")

    front_canvas.create_rectangle(230, 40, 320, 150, fill="white", outline="black")

    front_canvas.create_text(40, 60, text=name_entry.get(), anchor="w",
                              font=("Arial", 14, "bold"))

    front_canvas.create_text(40, 90, text=id_entry.get(), anchor="w", font=("Arial", 12))

    color = color_entry.get()

    try:
        front_canvas.create_rectangle(230, 160, 320, 190, fill=color)

    except:
        front_canvas.create_rectangle(230, 160, 320, 190, fill="gray")

    front_canvas.create_text(275, 175, text=status_entry.get())

    if photo_path:
        try:
            image = Image.open(photo_path)
            image = image.resize((90,110), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            front_canvas.create_image(275, 95, image=photo, anchor="center")

            front_canvas.photo =  photo

        except Exception as e:
            print(e)    


def draw_back():
    back_canvas.delete("all")

    back_canvas.create_rectangle(10, 10, 340, 210, fill="white", outline="black")   

    selected = []

    for var in events:
        if var.get() != "off":
            selected.append(var.get())

    print("Selected events:", selected)        

    event_text = "\n".join(selected)

    back_canvas.create_rectangle(20, 120, 170, 145, outline="black")

    back_canvas.create_text(25, 110, text="Signature", anchor="w")

    back_canvas.create_text(20, 50, text=event_text, anchor="nw",
                             width=150, font=("Arial", 12))

    back_canvas.create_text(20, 40, text="Participating Events", anchor="w",
                             font=("Arial", 14, "bold"))

    back_canvas.create_rectangle(180, 150, 320, 185, fill="black")   

    back_canvas.create_text(250, 195, text="Barcode")

def update_preview(event=None):
    draw_front()
    draw_back()

def resize_preview(event):
    front_canvas.config(
        width=event.width//2-20,
        height=event.height-30
        )
    back_canvas.config(
        width=event.width//2-20,
        height=event.height-30
        )
    update_preview()

preview_frame.bind("<Configure>",resize_preview)        

name_entry.bind("<KeyRelease>", update_preview)
id_entry.bind("<KeyRelease>",update_preview)
status_entry.bind("<KeyRelease>", update_preview)      
color_entry.bind("<KeyRelease>", update_preview)

events = []

event_names = ["3*3", "2*2", "4*4", "OH", "Pyraminx", "Skewb", "Clock"]

for name in event_names:
    var = ctk.StringVar(value="off")
    checkbox = ctk.CTkCheckBox(
        left_frame,
        text=name,
        variable=var,
        onvalue=name,
        offvalue="off",
        command=update_preview
    )
    checkbox.pack(anchor="w", padx=20)

    events.append(var)
update_preview()
app.mainloop()