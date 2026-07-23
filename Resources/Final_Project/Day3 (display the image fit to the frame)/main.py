from tkinter import filedialog
import customtkinter as ctk
from image_widgets import *
from PIL import Image, ImageTk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure the main application window
        self.title("CubeCanvas")
        self.geometry("1000x600")
        # self.minsize(800, 500)

        # Container used to stack and switch between pages
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        # Allow pages to expand with the window
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Create the application's pages
        self.page1 = ctk.CTkFrame(self.container)
        self.page2 = ctk.CTkFrame(self.container)

        # Place both pages in the same location for easy page switching
        self.page1.grid(row=0, column=0, sticky="nsew")
        self.page2.grid(row=0, column=0, sticky="nsew")

        # Automatically resize the displayed image whenever page2 changes size
        self.page2.bind("<Configure>", self.update_image)

        # Build widgets for both pages
        p1_open_button(self)
        p2_image_display(self)

        # Show the startup page
        self.show_page(self.page1)

    def show_page(self, page):
        # Bring the selected page to the front
        page.tkraise()

    def open_image(self):
        # Open file explorer and get the selected image path
        filepath = filedialog.askopenfilename()

        if not filepath:
            return

        # Store the original image so resizing always uses the full-quality version
        self.original_image = Image.open(filepath)

        # Display the image using the current window size
        self.update_image()

        # Switch to the image viewing page
        self.show_page(self.page2)

    def update_image(self, event=None):

        # Aspect Ratio Preserving Resize:
        # scale_w = frame_width  / image_width
        # scale_h = frame_height / image_height
        # scale   = min(scale_w, scale_h)
        #
        # new_width  = image_width  × scale
        # new_height = image_height × scale
        #
        # Using the smaller scale factor keeps the image proportions
        # unchanged while ensuring it fits within the available frame.


        # Prevent errors if no image has been loaded yet
        if not hasattr(self, "original_image"):
            return

        # Get the current size of the display area
        frame_width = self.page2.winfo_width()
        frame_height = self.page2.winfo_height()

        # Work on a copy to keep the original image unchanged
        image = self.original_image.copy()

        # Ignore resize events before the frame gets a valid size
        if frame_width <= 1 or frame_height <= 1:
            return

        image_width, image_height = self.original_image.size

        # Calculate the largest possible size while keeping proportions intact
        scale = min(
            frame_width / image_width,
            frame_height / image_height
        )

        # Compute the new dimensions after scaling
        new_width = int(image_width * scale)
        new_height = int(image_height * scale)

        # Resize the image using a high-quality scaling algorithm
        image = image.resize(
            (new_width, new_height),
            Image.Resampling.LANCZOS
        )

        # Convert the Pillow image into a Tkinter-compatible format
        self.tk_image = ImageTk.PhotoImage(image)

        # Replace the placeholder text with the resized image
        self.image_label.configure(
            image=self.tk_image,
            text=""
        )


app = App()

# Start the application's event loop
app.mainloop()