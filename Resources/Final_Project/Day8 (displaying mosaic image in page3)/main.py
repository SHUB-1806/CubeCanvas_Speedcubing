from tkinter import filedialog
import tkinter as tk
import customtkinter as ctk
from image_widgets import *
from PIL import Image, ImageTk

from image_processing import process_image
import numpy as np

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

        # Instantiate page 1, page 2, and page 3 as independent frame layouts nested inside the main container.
        self.page1 = ctk.CTkFrame(self.container)
        self.page2 = ctk.CTkFrame(self.container)
        self.page3 = ctk.CTkFrame(self.container)

        self.page1.grid(row=0,column=0,sticky="nsew")
        self.page2.grid(row=0,column=0,sticky="nsew")
        self.page3.grid(row=0,column=0,sticky="nsew")

        make_page1(self)
        make_page2(self)
        make_page3(self)

        self.canvas_image = None
        self.v_line = None
        self.h_line = None

        self.show_page(self.page1)

        self.crop_rect = None
        self.is_selecting = False

        self.start_x = None
        self.start_y = None

        self.crop_display_coords = None

        # Bind the enter key release event globally to instantly calculate and render the crop block mosaic view.
        self.bind("<Return>", self.confirm_crop)

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

        # A resize changes the canvas-to-image coordinate mapping, so an old
        # crop rectangle must not be confirmed with stale coordinates.
        self.crop_rect = None
        self.crop_display_coords = None

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

        x, y = event.x, event.y

        left, top = self.image_x, self.image_y
        right, bottom = (
            left + self.display_width,
            top + self.display_height
        )

        # Hide the green crosshair guide lines completely if the user moves their mouse outside image bounds.
        if not (left <= x <= right and top <= y <= bottom):
            self.hide_crosshair()
            return

        # Restore visibility for the vertical guide line tracking element when the cursor is over the image.
        for line in (self.v_line, self.h_line):
            self.image_canvas.itemconfigure(
                line,
                state="normal"
            )

        # Update the vertical line coordinates so it spans the entire height of the image at the cursor position.
        self.image_canvas.coords(
            self.v_line,
            x, top,
            x, bottom
        )

        # Update the horizontal line coordinates so it spans the entire width of the image at the cursor position.
        self.image_canvas.coords(
            self.h_line,
            left, y,
            right, y
        )

    def hide_crosshair(self, event=None):
        # Safely hide the horizontal and vertical cursor tracking lines from user view if they are initialized.
        for line in (self.v_line, self.h_line):
            if line is not None:
                self.image_canvas.itemconfigure(
                    line,
                    state="hidden"
                )

    def start_crop(self, event):
        # Validate that the click event occurred entirely inside the actual image boundaries before continuing.
        if not (
            self.image_x <= event.x <= self.image_x + self.display_width
            and
            self.image_y <= event.y <= self.image_y + self.display_height
        ):
            return

        self.is_selecting = True
        self.start_x = event.x
        self.start_y = event.y

        # Erase previous structural crop box items drawn on the viewport canvas to prevent graphic overlapping.
        if self.crop_rect is not None:
            self.image_canvas.delete(self.crop_rect)

        # Generate a brand-new selection box layout tracker that defaults to an initial width and height of zero.
        self.crop_rect = self.image_canvas.create_rectangle(
            event.x,
            event.y,
            event.x,
            event.y,
            outline="blue",
            width=3
        )


    def get_crop_ratio(self):
        try:
            # Read current values in row and column text widgets to form a basic dimensional aspect ratio float.
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())

            if rows <= 0 or cols <= 0:
                return None

            # Image aspect ratio is width / height: columns / rows.
            return cols / rows

        except ValueError:
            return None


    def update_crop(self, event):
        # Interrupt the update pipeline entirely if the selection state flag evaluates to false at runtime.
        if not self.is_selecting:
            return

        ratio = self.get_crop_ratio()

        if ratio is None:
            return

        dx = event.x - self.start_x
        dy = event.y - self.start_y

        sign_x = 1 if dx >= 0 else -1
        sign_y = 1 if dy >= 0 else -1

        width = abs(dx)
        height = abs(dy)

        if width / max(height, 1) > ratio:
            height = width / ratio
        else:
            width = height * ratio

        x = self.start_x + sign_x * width
        y = self.start_y + sign_y * height

        # Clip structural endpoint coordinates to ensure selection boxes remain constrained within canvas boundaries.
        x = min(
            max(x, self.image_x),
            self.image_x + self.display_width
        )

        # Enforce hard image baseline constraints on the vertical scaling axis to avoid out of bounds exceptions.
        y = min(
            max(y, self.image_y),
            self.image_y + self.display_height
        )

        # Reposition the drawn corner nodes of the active blue canvas selection rectangle object dynamically.
        self.image_canvas.coords(
            self.crop_rect,
            self.start_x,
            self.start_y,
            x,
            y
        )


    def finish_crop(self, event):
        # Break selection operations instantly if mouse button release event triggers out of chronological order.
        if not self.is_selecting:
            return

        self.is_selecting = False

        x1, y1, x2, y2 = self.image_canvas.coords(
            self.crop_rect
        )

        # Organize structural edge measurements cleanly into traditional left, top, right, bottom coordinate tuples.
        self.crop_display_coords = (
            min(x1, x2),
            min(y1, y2),
            max(x1, x2),
            max(y1, y2)
        )

        # print("Canvas coordinates:")
        # print(self.crop_display_coords)


    def confirm_crop(self, event=None):
        """
        Convert the selected crop region from canvas coordinates
        back to original image coordinates, generate the Rubik
        mosaic, and display the preview page.
        """

        # Interrupt confirmation processes immediately if no spatial crop area coordinates have been mapped out.
        if self.crop_display_coords is None:
            return

        # Crop coordinates on the displayed canvas image
        left, top, right, bottom = self.crop_display_coords

        # Scale factors between displayed image and original image
        scale_x = (
            self.original_image.width
            / self.display_width
        )

        scale_y = (
            self.original_image.height
            / self.display_height
        )

        # Convert canvas coordinates to original image coordinates
        x1 = int(
            (left - self.image_x) * scale_x
        )

        y1 = int(
            (top - self.image_y) * scale_y
        )

        x2 = int(
            (right - self.image_x) * scale_x
        )

        y2 = int(
            (bottom - self.image_y) * scale_y
        )

        # Crop the original image using the calculated coordinates
        self.cropped_image = self.original_image.crop(
            (x1, y1, x2, y2)
        )

        #
        # Build the Rubik colour palette from the colour entries
        #
        palette = []

        for box, entry in self.color_widgets:

            try:
                # Remove '#' from hexadecimal colour code
                color = entry.get().lstrip("#")

                # Convert hex colour to RGB
                rgb = [
                    int(color[i:i+2], 16)
                    for i in (0, 2, 4)
                ]

                palette.append(rgb)

            except:
                # Ignore invalid colour inputs
                pass

        palette = np.array(
            palette,
            dtype=np.uint8
        )

        #
        # Read the cube dimensions entered by the user
        #
        rows = int(self.rows_entry.get())
        cols = int(self.cols_entry.get())

        #
        # Generate the processed Rubik mosaic image
        #
        self.processed_image = process_image(
            self.cropped_image,
            palette,
            rows,
            cols
        )

        # Update preview canvases on Page 3
        self.update_page3_images()

        # Navigate to the preview page
        self.show_page(self.page3)


    def fit_image_canvas(self, image, canvas, force_size=None):
        """
        Resize an image to fit inside the given canvas while
        preserving its aspect ratio.
        """

        # Ensure the canvas dimensions are updated
        canvas.update_idletasks()

        w = canvas.winfo_width()
        h = canvas.winfo_height()

        # Ignore invalid canvas sizes
        if w <= 1 or h <= 1:
            return

        # Original image dimensions
        iw, ih = image.size

        # Scale image to fit within the canvas
        if force_size is None:
            scale = min(w / iw, h / ih)

            nw = int(iw * scale)
            nh = int(ih * scale)

        else:
            nw, nh = force_size

        # Use NEAREST to preserve the pixelated appearance
        resized = image.resize(
            (nw, nh),
            Image.Resampling.NEAREST
        )

        tk_img = ImageTk.PhotoImage(resized)

        # Remove any previously displayed image
        canvas.delete("all")

        # Keep a reference to prevent garbage collection
        canvas.image_ref = tk_img

        # Display the image centered inside the canvas
        canvas.create_image(
            (w - nw) // 2,
            (h - nh) // 2,
            anchor="nw",
            image=tk_img
        )


    def update_page3_images(self, event=None):

        if not hasattr(self, "cropped_image"):
            return

        #
        # Calculate display size from cropped image
        #
        self.crop_canvas.update_idletasks()

        cw = self.crop_canvas.winfo_width()
        ch = self.crop_canvas.winfo_height()

        iw, ih = self.cropped_image.size

        scale = min(cw / iw, ch / ih)

        nw = int(iw * scale)
        nh = int(ih * scale)

        #
        # Display both images using EXACTLY
        # the same display dimensions
        #
        self.fit_image_canvas(
            self.cropped_image,
            self.crop_canvas,
            force_size=(nw, nh)
        )

        self.fit_image_canvas(
            self.processed_image,
            self.process_canvas,
            force_size=(nw, nh)
        )

app = App()
app.mainloop()
