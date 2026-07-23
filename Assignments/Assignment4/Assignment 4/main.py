from tkinter import filedialog, colorchooser
import tkinter as tk
import customtkinter as ctk
from image_widgets import *
from PIL import Image, ImageTk
from image_processing import apply_effects, process_image, blur_mosaic, show_histogram
import numpy as np

from pdf_export import export_pdf


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set title to CubeCanvas and establish a starting application window size of 1000x600 pixels.
        self.title("CubeCanvas")
        self.geometry("1000x600")

        #Question 4:Undo & Redo Stacks
        self.undo_stack = []
        self.redo_stack = []
        self.selected_dither_method = "Nearest Color"
        self.selected_cube_size = 3

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

        # Place all three page layouts at identical grid coordinates so they overlap and fill the framework space.
        self.page1.grid(row=0, column=0, sticky="nsew")
        self.page2.grid(row=0, column=0, sticky="nsew")
        self.page3.grid(row=0, column=0, sticky="nsew")

        # Invoke external helper layout functions to populate all three functional frames with distinct elements.
        make_page1(self)
        make_page2(self)
        make_page3(self)

        # Bring the primary image selection frame layer to the absolute front of the display stack on startup.
        self.show_page(self.page1)

    def show_page(self, page):
        # Pull the requested page frame layout to the front of the screen stack to make it visible.
        page.tkraise()

    def open_image(self):
        # Open a native system file explorer dialog box and capture the selected local file path string.
        filepath = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.webp")]
        )

        # Check if the path string is empty, indicating that the user closed or canceled the file picker.
        if not filepath:
            return

        # Load the chosen file from disk and store it in memory as an unscaled persistent PIL Image object.
        self.original_image = Image.open(filepath)
        self.crop_box = None
        self.show_page(self.page2)

        # Resize and render the selected image asset inside the available view panel frame dimensions.
        self.update_image()

    def update_image(self, *args):
        # Terminate early to prevent processing errors if the source image attribute has not been loaded.
        if not hasattr(self, "original_image"):
            return
        
        canvas_width = self.image_canvas.winfo_width()
        canvas_height = self.image_canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            return
        
        img_width, img_height = self.original_image.size
        scale = min(canvas_width / img_width,canvas_height / img_height)

        new_width = int(img_width * scale)
        new_height = int(img_height * scale)

        self.scale = scale

        resized_image = self.original_image.resize(
            (new_width, new_height), Image.Resampling.LANCZOS
        )

        self.tk_image = ImageTk.PhotoImage(resized_image)

        self.image_canvas.delete("all")

        self.offset_x = (canvas_width - new_width) // 2
        self.offset_y = (canvas_height - new_height) // 2

        self.image_canvas.create_image(
            self.offset_x,self.offset_y,anchor="nw",image=self.tk_image
        )

        self.draw_grid()

        if self.crop_box:
            self.image_canvas.create_rectangle(
                self.crop_box[0],
                self.crop_box[1],
                self.crop_box[2],
                self.crop_box[3],
                outline="red",
                width=2
            )

    def update_cube_count(self, event=None):
        try:
            # Parse text input values from the row and column entry boxes and cast them into valid integers.
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
            total = rows * cols
            self.total_label.configure(text=f"=   {total} Cubes")

            if hasattr(self, "original_image"):
                self.draw_grid()
        # Catch data conversion exceptions caused by empty or text inputs and safely set the total to zero.
        except ValueError:
            self.total_label.configure(text="=  0 Cubes")

    def draw_grid(self):
        if not hasattr(self, "scale"):
            return

        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
        except ValueError:
            return

        if rows <= 0 or cols <= 0:
            return

        img_w, img_h = self.original_image.size
        disp_w = img_w * self.scale
        disp_h = img_h * self.scale

        start_x = self.offset_x
        start_y = self.offset_y

        cell_w = disp_w / cols
        cell_h = disp_h / rows

        for r in range(rows + 1):
            y = start_y + r * cell_h
            self.image_canvas.create_line(
                start_x, y, start_x + disp_w, y, fill="yellow", width=1
            )

        for c in range(cols + 1):
            x = start_x + c * cell_w
            self.image_canvas.create_line(
                x, start_y, x, start_y + disp_h, fill="yellow", width=1
            )

    def start_crop(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.crop_box = [event.x, event.y, event.x, event.y]

    def update_crop(self, event):
        self.crop_box[2] = event.x
        self.crop_box[3] = event.y
        self.update_image()

    def finish_crop(self, event):
        x1, y1, x2, y2 = self.crop_box

        x1 = min(x1, x2)
        x2 = max(self.start_x, event.x)
        y1 = min(y1, y2)
        y2 = max(self.start_y, event.y)

        x1 -= self.offset_x
        x2 -= self.offset_x
        y1 -= self.offset_y
        y2 -= self.offset_y

        img_x1 = max(0, int(x1 / self.scale))
        img_y1 = max(0, int(y1 / self.scale))
        img_x2 = min(self.original_image.width, int(x2 / self.scale))
        img_y2 = min(self.original_image.height, int(y2 / self.scale))

        if img_x2 > img_x1 and img_y2 > img_y1:
            self.cropped_image = self.original_image.crop(
                (img_x1, img_y1, img_x2, img_y2)
            )
            self.preview_image = self.cropped_image.copy()

            self.update_palette_from_entries()
            self.push_state()
            self.show_page(self.page3)
            self.apply_page3_effects()

    def update_palette_from_entries(self):
        palette = []
        for _, entry in self.color_widgets:
            hex_color = entry.get().strip()
            if hex_color.startswith("#") and len(hex_color) == 7:
                r = int(hex_color[1:3], 16)
                g = int(hex_color[3:5], 16)
                b = int(hex_color[5:7], 16)
                palette.append([r, g, b])

        if palette:
            self.palette = np.array(palette)

    def apply_page3_effects(self, val=None):
        if not hasattr(self, "cropped_image"):
            return

        b = self.brightness_slider.get()
        c = self.contrast_slider.get()
        s = self.saturation_slider.get()
        sh = self.sharpness_slider.get()
        bl = self.blur_slider.get()

        fx = self.flip_x_switch.get()
        fy = self.flip_y_switch.get()

        self.preview_image = apply_effects(
            self.cropped_image,
            brightness=b,
            contrast=c,
            saturation=s,
            sharpness=sh,
            blur=bl,
            flip_horizontal=fx,
            flip_vertical=fy
        )

        rows = int(self.rows_entry.get())
        cols = int(self.cols_entry.get())

        method = getattr(self, "selected_dither_method", "Nearest Color")
        cube_size = getattr(self, "selected_cube_size", 3)

        self.processed_image = process_image(
            self.preview_image,
            self.palette,
            rows,
            cols,
            method=method,
            cube_size=cube_size
        )

        if self.blur_mosaic_switch.get():
            self.processed_image = blur_mosaic(self.processed_image, radius=1)

        self.update_page3_images()

    def update_page3_images(self, event=None):
        if not hasattr(self, "preview_image") or not hasattr(self, "processed_image"):
            return

        w1 = self.crop_canvas.winfo_width()
        h1 = self.crop_canvas.winfo_height()

        if w1 > 1 and h1 > 1:
            img1 = self.preview_image.copy()
            img1.thumbnail((w1, h1), Image.Resampling.LANCZOS)
            self.tk_crop = ImageTk.PhotoImage(img1)
            self.crop_canvas.delete("all")
            self.crop_canvas.create_image(
                w1 // 2, h1 // 2, anchor="center", image=self.tk_crop
            )

        w2 = self.process_canvas.winfo_width()
        h2 = self.process_canvas.winfo_height()

        if w2 > 1 and h2 > 1:
            img2 = self.processed_image.copy()
            img2.thumbnail((w2, h2), Image.Resampling.NEAREST)
            self.tk_process = ImageTk.PhotoImage(img2)
            self.process_canvas.delete("all")
            self.process_canvas.create_image(
                w2 // 2, h2 // 2, anchor="center", image=self.tk_process
            )

    def move_crosshair(self, event):
        self.image_canvas.delete("crosshair")
        w = self.image_canvas.winfo_width()
        h = self.image_canvas.winfo_height()

        self.image_canvas.create_line(
            0, event.y, w, event.y, fill="red", tags="crosshair"
        )
        self.image_canvas.create_line(
            event.x, 0, event.x, h, fill="red", tags="crosshair"
        )

    def hide_crosshair(self, event):
        self.image_canvas.delete("crosshair")

    def revert_changes(self):
        self.brightness_slider.set(1.0)
        self.contrast_slider.set(1.0)
        self.saturation_slider.set(1.0)
        self.sharpness_slider.set(1.0)
        self.blur_slider.set(0)

        self.flip_x_switch.deselect()
        self.flip_y_switch.deselect()
        self.blur_mosaic_switch.deselect()

        self.apply_page3_effects()

    # --- QUESTION 4: Undo & Redo ---
    def push_state(self):
        if hasattr(self, "preview_image") and self.preview_image is not None:
            self.undo_stack.append(self.preview_image.copy())
            self.redo_stack.clear()

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(self.preview_image.copy())
            self.preview_image = self.undo_stack.pop()
            self.apply_page3_effects()

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.preview_image.copy())
            self.preview_image = self.redo_stack.pop()
            self.apply_page3_effects()

    # --- QUESTION 1: RGB Histogram ---
    def trigger_histogram(self):
        if hasattr(self, "preview_image") and self.preview_image is not None:
            show_histogram(self.preview_image)

    # --- QUESTION 6: Color Chooser ---
    def pick_color_for_swatch(self, entry_widget, swatch_frame):
        current_color = entry_widget.get()
        color = colorchooser.askcolor(initialcolor=current_color)
        if color[1]:
            hex_val = color[1]
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, hex_val)
            swatch_frame.configure(fg_color=hex_val)
            self.update_palette_from_entries()

    # --- QUESTION 3 & 5: Dithering & Cube Size Handlers ---
    def on_dither_change(self, choice):
        self.selected_dither_method = choice
        self.apply_page3_effects()

    def on_cube_size_change(self, choice):
        self.selected_cube_size = int(choice.split("x")[0])
        self.apply_page3_effects()

    def export_current_pdf(self):
        if not hasattr(self, "processed_image"):
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Export PDF"
        )

        if not filepath:
            return
        
        try:
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())
        except ValueError:
            rows, cols = 1, 1    

        cube_size = getattr(self, "selected_cube_size", 3)

        pages = export_pdf(
            self.processed_image,
            rows,
            cols,
            cube_size=cube_size
        )

        pages[0].save(
            filepath,
            save_all=True,
            append_images=pages[1:],
            format="PDF",
            resolution=100
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()          
