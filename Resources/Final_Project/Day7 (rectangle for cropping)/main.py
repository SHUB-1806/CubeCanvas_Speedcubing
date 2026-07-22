# <Double-Button-1>
# ↓
# Double left click

# <B1-Motion>
# ↓
# Mouse moves while left button held

# <ButtonRelease-1>
# ↓
# Left mouse released


from tkinter import filedialog
import tkinter as tk
import customtkinter as ctk
from image_widgets import *
from PIL import Image, ImageTk


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CubeCanvas")
        self.geometry("1000x600")

        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.page1 = ctk.CTkFrame(self.container)
        self.page2 = ctk.CTkFrame(self.container)

        self.page1.grid(row=0, column=0, sticky="nsew")
        self.page2.grid(row=0, column=0, sticky="nsew")

        make_page1(self)
        make_page2(self)

        self.canvas_image = None
        self.v_line = None
        self.h_line = None

        self.show_page(self.page1)

        # Crop selection state
        self.crop_rect = None
        self.is_selecting = False

        # Crop drag start point
        self.start_x = None
        self.start_y = None

        # Final crop rectangle (canvas coordinates)
        self.crop_display_coords = None

        self.bind("<Return>", self.confirm_crop)

    def show_page(self, page):
        page.tkraise()

    def open_image(self):
        filepath = filedialog.askopenfilename()

        if not filepath:
            return

        self.original_image = Image.open(filepath)

        self.update_image()

        self.show_page(self.page2)

    def update_image(self, event=None):
        if not hasattr(self, "original_image"):
            return

        self.fit_image_to_frame(
            self.original_image,
            self.image_panel,
            self.image_canvas
        )

    def fit_image_to_frame(self, image, frame, canvas):
        frame_width = frame.winfo_width()
        frame_height = frame.winfo_height()

        if frame_width <= 1 or frame_height <= 1:
            return

        img_width, img_height = image.size

        scale = min(
            frame_width / img_width,
            frame_height / img_height
        )

        new_width = int(img_width * scale)
        new_height = int(img_height * scale)

        resized = image.resize(
            (new_width, new_height),
            Image.Resampling.LANCZOS
        )

        self.tk_image = ImageTk.PhotoImage(resized)

        canvas.delete("all")

        # A resize changes the canvas-to-image coordinate mapping, so an old
        # crop rectangle must not be confirmed with stale coordinates.
        self.crop_rect = None
        self.crop_display_coords = None

        self.display_width = new_width
        self.display_height = new_height

        self.image_x = (frame_width - new_width) // 2
        self.image_y = (frame_height - new_height) // 2

        self.canvas_image = canvas.create_image(
            self.image_x,
            self.image_y,
            anchor="nw",
            image=self.tk_image
        )

        self.v_line = canvas.create_line(
            0, 0, 0, 0,
            fill="green",
            width=2,
            state="hidden"
        )

        self.h_line = canvas.create_line(
            0, 0, 0, 0,
            fill="green",
            width=2,
            state="hidden"
        )

    def update_cube_count(self, event=None):
        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())

            total = rows * cols

        except ValueError:
            total = 0

        self.total_label.configure(
            text=f"=   {total} Cubes"
        )

    def move_crosshair(self, event):
        # Crosshair lines are created only after an image is displayed
        if self.v_line is None:
            return

        # Current mouse position on the canvas
        x = event.x
        y = event.y

        # Displayed image boundaries on the canvas
        left = self.image_x
        top = self.image_y
        right = left + self.display_width
        bottom = top + self.display_height

        # Hide the crosshair when the cursor leaves the image area
        if not (left <= x <= right and top <= y <= bottom):
            self.hide_crosshair()
            return

        # Make the guide lines visible
        self.image_canvas.itemconfigure(
            self.v_line,
            state="normal"
        )

        self.image_canvas.itemconfigure(
            self.h_line,
            state="normal"
        )

        # Vertical line spans the full displayed image height
        self.image_canvas.coords(
            self.v_line,
            x,
            top,
            x,
            bottom
        )

        # Horizontal line spans the full displayed image width
        self.image_canvas.coords(
            self.h_line,
            left,
            y,
            right,
            y
        )

    def hide_crosshair(self, event=None):
        # Hide the vertical guide line
        if self.v_line is not None:
            self.image_canvas.itemconfigure(
                self.v_line,
                state="hidden"
            )

        # Hide the horizontal guide line
        if self.h_line is not None:
            self.image_canvas.itemconfigure(
                self.h_line,
                state="hidden"
            )

    def start_crop(self, event):
        # Only allow crop selection to begin inside the image
        if not (
            self.image_x <= event.x <= self.image_x + self.display_width
            and
            self.image_y <= event.y <= self.image_y + self.display_height
        ):
            return

        # Enter crop-selection mode
        self.is_selecting = True

        # Remember where the drag started
        self.start_x = event.x
        self.start_y = event.y

        # Remove any previously drawn crop rectangle
        if self.crop_rect is not None:
            self.image_canvas.delete(self.crop_rect)

        # Create a new rectangle that will expand as the mouse moves
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
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())

            if rows <= 0 or cols <= 0:
                return None

            # Image aspect ratio is width / height: columns / rows.
            return cols / rows

        except ValueError:
            return None

    def update_crop(self, event):
        # Ignore drag events unless a crop is currently active
        if not self.is_selecting:
            return

        # Desired aspect ratio from the topbar entries
        ratio = self.get_crop_ratio()

        # Cannot continue without a valid ratio
        if ratio is None:
            return

        # Mouse movement relative to the drag start point
        dx = event.x - self.start_x
        dy = event.y - self.start_y

        # Remember the drag direction so the user can drag
        # in any of the four directions.
        sign_x = 1 if dx >= 0 else -1
        sign_y = 1 if dy >= 0 else -1

        width = abs(dx)
        height = abs(dy)

        """
        Enforce the requested aspect ratio.

        If the dragged rectangle is too wide,
        adjust the height.

        If it is too tall,
        adjust the width.

        This ensures:

            width / height == rows / cols
        """
        if width / max(height, 1) > ratio:
            height = width / ratio
        else:
            width = height * ratio

        # Reconstruct the rectangle using the original drag direction
        x = self.start_x + sign_x * width
        y = self.start_y + sign_y * height

        # Prevent the crop window from extending beyond the image
        x = min(
            max(x, self.image_x),
            self.image_x + self.display_width
        )

        y = min(
            max(y, self.image_y),
            self.image_y + self.display_height
        )

        # Update the rectangle coordinates on the canvas
        self.image_canvas.coords(
            self.crop_rect,
            self.start_x,
            self.start_y,
            x,
            y
        )

    def finish_crop(self, event):
        # Ignore release events if no crop was active
        if not self.is_selecting:
            return

        # Exit crop-selection mode
        self.is_selecting = False

        # Get the rectangle coordinates from the canvas
        x1, y1, x2, y2 = self.image_canvas.coords(
            self.crop_rect
        )

        """
        Normalize the coordinates.

        Since the user can drag in any direction,
        x2 may be smaller than x1 and vice versa.

        Store them consistently as:

            left, top, right, bottom
        """
        self.crop_display_coords = (
            min(x1, x2),
            min(y1, y2),
            max(x1, x2),
            max(y1, y2)
        )

        print("Canvas coordinates:")
        print(self.crop_display_coords)

    def confirm_crop(self, event=None):
        # No finalized crop rectangle exists yet
        if self.crop_display_coords is None:
            return

        left, top, right, bottom = (
            self.crop_display_coords
        )

        """
        The displayed image is usually a scaled version
        of the original image.

        Compute the conversion factors between:

            displayed image pixels
                    ↓
            original image pixels
        """
        scale_x = (
            self.original_image.width
            / self.display_width
        )

        scale_y = (
            self.original_image.height
            / self.display_height
        )

        # Convert canvas coordinates back to original image coordinates
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

        print("Original image coordinates:")
        print(x1, y1, x2, y2)

        # These coordinates can be passed directly to:
        # self.original_image.crop((x1, y1, x2, y2))

app = App()
app.mainloop()
