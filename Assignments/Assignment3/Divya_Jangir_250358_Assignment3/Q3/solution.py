# 1. We use min() so the image fits completely inside the given width and height without being cropped.Using max() may make one side larger than the frame.

# 2. Python's Garbage Collector removes objects that are no longer referenced. If we do not store a reference to ImageTk.PhotoImage, it may be garbage collected and the image disappears from the Tkinter window.

from PIL import Image, ImageTk
import customtkinter as ctk

def safe_resize(image_path, max_w, max_h):
    image = Image.open(image_path)

    img_w, img_h = image.size

    scale = min(max_w / img_w, max_h / img_h)

    new_w = int(img_w * scale)
    new_h = int(img_h * scale)

    resized = image.resize((new_w, new_h), Image.Resampling.LANCZOS)

    return resized, (new_w, new_h)

def update_image(event):
    max_w = event.width - 20
    max_h = event.height - 70

    image, size = safe_resize("Shinchan.jpg", max_w, max_h)

    photo = ImageTk.PhotoImage(image)

    label.configure(image=photo)
    label.image = photo

    size_label.configure(text=f"New Size:{size}")

app = ctk.CTk()
app.title("Question 3")
app.geometry("600*500")

label = ctk.CTkLabel(app, text="")
label.pack(pady=10)

size_label = ctk.CTkLabel(app, text="")
size_label.pack()

app.bind("<Configure>", update_image)

app.mainloop()