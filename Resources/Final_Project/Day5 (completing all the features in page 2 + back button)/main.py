from tkinter import filedialog
import customtkinter as ctk
from image_widgets import *
from PIL import Image, ImageTk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set title to CubeCanvas and establish a starting application window size of 1000x600 pixels.
        self.title("CubeCanvas")
        self.geometry("1000x600")
        # self.minsize(800, 500)

        # Create a central structural frame container that will hold and manage all stacked application pages.
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        # Configure the grid system so that row 0 and column 0 expand dynamically when resizing the window.
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Instantiate page 1 and page 2 as independent frame layouts nested inside the main container.
        self.page1 = ctk.CTkFrame(self.container)
        self.page2 = ctk.CTkFrame(self.container)

        # Place both page frames at identical coordinates so they overlap and fill the layout space entirely.
        self.page1.grid(row=0, column=0, sticky="nsew")
        self.page2.grid(row=0, column=0, sticky="nsew")

        # Invoke external helper functions to populate both page frames with their sub-widgets and buttons.
        make_page1(self)
        make_page2(self)

        # Bring the primary image selection frame to the front layer of the user interface on startup.
        self.show_page(self.page1)

    def show_page(self, page):
        # Bring the requested page frame layout to the front of the screen stack to make it visible.
        page.tkraise()

    def open_image(self):
        # Open a native system file explorer dialog box and capture the selected local file path string.
        filepath = filedialog.askopenfilename()

        # Check if the path string is empty, indicating that the user closed or canceled the file picker.
        if not filepath:
            return

        # Load the chosen file from disk and store it in memory as an unscaled persistent PIL Image object.
        self.original_image = Image.open(filepath)

        # Resize and render the selected image asset inside the available view panel frame dimensions.
        self.update_image()

        # Switch the active visible view frame to page 2 to reveal the editing and panel dashboard area.
        self.show_page(self.page2)

    def update_image(self, event=None):

        # Terminate early to prevent processing errors if the source image attribute has not been loaded.
        if not hasattr(self, "original_image"):
            return

        # Pass the original asset and layout targets to the scaling logic function to refresh the display.
        self.fit_image_to_frame(
            self.original_image,
            self.image_panel,
            self.image_label
        )

    def fit_image_to_frame(self, image, frame, label):

        # Aspect Ratio Preserving Resize formula logic: compute width scale (frame_w / img_w), height scale (frame_h / img_h), select the minimum factor, and multiply the original dimensions by it

        # Read the current bounding width and height layout measurements directly from the parent frame.
        frame_width = frame.winfo_width()
        frame_height = frame.winfo_height()

        # Exit if the panel dimensions have not resolved past baseline placeholder values during layout.
        if frame_width <= 1 or frame_height <= 1:
            return

        # Extract the intrinsic structural width and height dimensions directly from the source image asset.
        img_width, img_height = image.size

        # Find the uniform scaling multiplier by selecting the lesser value between the width and height ratios.
        scale = min(
            frame_width / img_width,
            frame_height / img_height
        )

        # Calculate the proportional bounding coordinates for the new canvas size using the scale factor.
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)

        # Create a copy resized with high-fidelity Lanczos filtering to minimize image blur and distortion.
        resized = image.resize(
            (new_width, new_height),
            Image.Resampling.LANCZOS
        )

        # Convert the processed PIL photo instance into an image format that Tkinter can natively render.
        tk_image = ImageTk.PhotoImage(resized)

        # Apply the final processed Tkinter image to the target display label and clear its structural text.
        label.configure(
            image=tk_image,
            text=""
        )

        # Bind a reference of the image asset directly to the label widget instance to avoid garbage collection.
        label.image = tk_image

    # Read grid dimensions and calculate the total block count to display on the top bar of page 2.
    def update_cube_count(self, event=None):

        try:
            # Parse text input values from the row and column entry boxes and cast them into valid integers.
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())

            # Multiply the valid row and column dimensions to obtain the total count of mosaic cube units.
            total = rows * cols

        # Catch data conversion exceptions caused by empty or text inputs and safely set the total to zero.
        except ValueError:
            total = 0

        # Update the text attribute of the tracking label with the newly calculated total block count.
        self.total_label.configure(
            text=f"=   {total} Cubes"
        )


# Instantiate the main App framework class containing the window configuration and logic structures.
app = App()

# Run the core Tkinter layout loop to intercept application event signals and keep the window open.
app.mainloop()