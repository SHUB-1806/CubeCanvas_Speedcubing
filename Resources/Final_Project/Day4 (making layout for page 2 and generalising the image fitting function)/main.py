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

        # Container frame used to hold and switch between different pages
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        # Allow pages inside the container to resize with the window
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Create the application's pages
        self.page1 = ctk.CTkFrame(self.container)
        self.page2 = ctk.CTkFrame(self.container)

        # Stack both pages at the same position and show one at a time
        self.page1.grid(row=0, column=0, sticky="nsew")
        self.page2.grid(row=0, column=0, sticky="nsew")

        # Build widgets for both pages
        make_page1(self)
        make_page2(self)

        # Display the startup page
        self.show_page(self.page1)

    def show_page(self, page):
        # Bring the selected page to the front
        page.tkraise()

    def open_image(self):
        # Open a file picker and return the selected image path
        filepath = filedialog.askopenfilename()

        # Stop execution if the user closes the dialog without selecting a file
        if not filepath:
            return

        # Store the original image so future resizing always uses full quality
        self.original_image = Image.open(filepath)

        # Display the image using the current frame dimensions
        self.update_image()

        # Navigate to the image viewing page
        self.show_page(self.page2)

# changed this function to make it generalized
    def update_image(self, event=None):

        # Prevent errors if an image has not been loaded yet
        if not hasattr(self, "original_image"):
            return

        # Delegate image fitting to a reusable helper function
        self.fit_image_to_frame(
            self.original_image,
            self.image_panel,
            self.image_label
        )

# generalised image fitting function
    def fit_image_to_frame(self,image,frame,label):
        """
        image : PIL.Image
        frame : widget whose size we want to fit into
        label : CTkLabel where image is displayed
        """

        # Aspect Ratio Preserving Resize:
        # scale_w = frame_width  / image_width
        # scale_h = frame_height / image_height
        # scale   = min(scale_w, scale_h)
        #
        # new_width  = image_width  × scale
        # new_height = image_height × scale
        #
        # Using the smaller scale factor ensures the entire image
        # fits inside the frame without distortion or cropping.

        # Get the current dimensions of the target frame
        frame_width = frame.winfo_width()
        frame_height = frame.winfo_height()

        # Ignore resize attempts before the frame receives a valid size
        if frame_width <= 1 or frame_height <= 1:
            return

        # Read the original image dimensions
        img_width, img_height = image.size

        # Compute a scale factor that preserves the image's aspect ratio
        scale = min(
            frame_width / img_width,
            frame_height / img_height
        )

        # Calculate the resized dimensions
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)

        # Resize using a high-quality resampling algorithm
        resized = image.resize(
            (new_width, new_height),
            Image.Resampling.LANCZOS
        )

        # Convert the Pillow image into a format Tkinter can display
        tk_image = ImageTk.PhotoImage(resized)
        
        # this configure thing just locally updates the thing
        label.configure(
            image=tk_image,
            text=""
        )

        # hence we have to store it manually too
        # Keeping a reference prevents Tkinter from garbage collecting the image
        label.image = tk_image

app = App()

# Start the GUI event loop
app.mainloop()