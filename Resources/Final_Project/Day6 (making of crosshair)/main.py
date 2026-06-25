from tkinter import filedialog
import tkinter as tk
import customtkinter as ctk
from image_widgets import *
from PIL import Image, ImageTk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set title to CubeCanvas and establish a starting application window size of 1000x600 pixels.
        self.title("CubeCanvas")
        self.geometry("1000x600")

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

        # Initialize state variables to track the rendered image and the visual crosshair line components.
        self.canvas_image = None
        self.v_line = None
        self.h_line = None

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
            self.image_canvas
        )

    def fit_image_to_frame(self, image, frame, canvas):
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
        self.tk_image = ImageTk.PhotoImage(resized)

        # Clear all existing drawing items from the canvas before rendering the newly updated image.
        canvas.delete("all")

        # Store the computed visual display dimensions to bound cursor tracking limits later in the code.
        self.display_width = new_width
        self.display_height = new_height

        # Calculate the appropriate centering offsets to position the image directly in the middle of the canvas.
        self.image_x = (frame_width - new_width) // 2
        self.image_y = (frame_height - new_height) // 2

        # Render the final Tkinter image to the canvas using the calculated offsets and store its reference.
        self.canvas_image = canvas.create_image(
            self.image_x,
            self.image_y,
            anchor="nw",
            image=self.tk_image
        )

        # Instantiate a hidden vertical green line on the canvas that will later follow the user cursor.
        self.v_line = canvas.create_line(
            0, 0, 0, 0,
            fill="green",
            width=2,
            state="hidden"
        )

        # Instantiate a hidden horizontal green line on the canvas that will later follow the user cursor.
        self.h_line = canvas.create_line(
            0, 0, 0, 0,
            fill="green",
            width=2,
            state="hidden"
        )

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

    def move_crosshair(self, event):
        # Abort crosshair rendering logic if the reference line objects have not been instantiated yet.
        if self.v_line is None:
            return

        # Capture the current live x and y coordinate positions of the mouse directly from the canvas event.
        x = event.x
        y = event.y

        # Establish the hard boundary coordinate limits of the active image rendered on the canvas space.
        left = self.image_x
        top = self.image_y
        right = left + self.display_width
        bottom = top + self.display_height

        # Hide the green crosshair guide lines completely if the user moves their mouse outside image bounds.
        if not (left <= x <= right and top <= y <= bottom):
            self.hide_crosshair()
            return

        # Restore visibility for the vertical guide line tracking element when the cursor is over the image.
        self.image_canvas.itemconfigure(
            self.v_line,
            state="normal"
        )

        # Restore visibility for the horizontal guide line tracking element when the cursor is over the image.
        self.image_canvas.itemconfigure(
            self.h_line,
            state="normal"
        )

        # Update the vertical line coordinates so it spans the entire height of the image at the cursor position.
        self.image_canvas.coords(
            self.v_line,
            x,
            top,
            x,
            bottom
        )

        # Update the horizontal line coordinates so it spans the entire width of the image at the cursor position.
        self.image_canvas.coords(
            self.h_line,
            left,
            y,
            right,
            y
        )

    def hide_crosshair(self, event=None):
        # Safely hide the vertical cursor tracking line from the user view if it exists in the active canvas.
        if self.v_line is not None:
            self.image_canvas.itemconfigure(
                self.v_line,
                state="hidden"
            )

        # Safely hide the horizontal cursor tracking line from the user view if it exists in the active canvas.
        if self.h_line is not None:
            self.image_canvas.itemconfigure(
                self.h_line,
                state="hidden"
            )

app = App()
app.mainloop()