'''
1. We use min instead of max so that the smaller ration can be used so the entire scaled image fits. If we use max, the larger scaled side will go outside the page and be cropped.
2. Python garbage collection is python's automatic memory management system. It automatically frees the memory used by objects that are no longer being referenced anywhere in the program. If we don't have an explicit reference to our image, garbage collection will automatically delete the image once it is done being used in a function.
'''

from PIL import Image, ImageTk
import customtkinter as ctk


def safe_resize(image_path, max_w, max_h):
    image = Image.open(image_path)

    original_width, original_height = image.size

    scale = min(max_w / original_width, max_h / original_height)

    new_width = int(original_width * scale)
    new_height = int(original_height * scale)

    resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    app = ctk.CTk()
    app.title("Question 3")
    app.geometry(f"{new_width}x{new_height}")

    tk_image = ImageTk.PhotoImage(resized)

    label = ctk.CTkLabel(app, image = tk_image, text="")
    label.pack(fill="both", expand=True)

    label.image = tk_image

    app.mainloop()

    return (new_width, new_height)

dimensions = safe_resize("4k-Marvels-Spider-Man-2-Miles-Morales-Peter-Parker-4K-Wallpaper.jpg", 1000, 600)
print("New Dimensions:", dimensions)