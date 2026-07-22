import tkinter as tk
import customtkinter as ctk
from image_widgets import *
from PIL import Image, ImageTk  # Used for loading and displaying image files


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure the main application window
        self.title("CubeCanvas")
        self.geometry("1000x600")
        # self.minsize(800, 500)

        # Container frame that stores all application pages
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        # Allow pages inside the container to resize with the window
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # -------Pages----------
        # Create page 1 and page 2 as separate frames
        self.page1 = ctk.CTkFrame(self.container)
        self.page2 = ctk.CTkFrame(self.container)

        # Place both pages in the same grid location for page switching
        self.page1.grid(row=0, column=0, sticky="nsew")
        self.page2.grid(row=0, column=0, sticky="nsew")

        # Build widgets for both pages using external functions
        p1_open_button(self)
        p2_image_display(self)

        # Display page 1 when the application starts
        self.show_page(self.page1)

    def show_page(self, page):
        # Bring the selected page to the front and make it visible
        page.tkraise()

    def open_image(self):

        # Open a file picker dialog and get the selected file path
        filepath = tk.filedialog.askopenfilename()

        if not filepath:    # to not move forward if someone didnt select any image, by not using this {if} we may get empty string
            return

        # Load the selected image using Pillow
        image = Image.open(filepath)

        # Convert Pillow image into a Tkinter-compatible image object
        self.tk_image = ImageTk.PhotoImage(image)

        # display it on page 2 inside the image_label space created forr it
        # configure basically means replace the properties already created, thats why the text "No Image" is replace by ""
        self.image_label.configure(image=self.tk_image, text="")

        # Switch to page 2 after the image is successfully loaded
        self.show_page(self.page2)


app = App()

# Start the Tkinter event loop and keep the application running
app.mainloop()