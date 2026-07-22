from tkinter import filedialog
import tkinter as tk
import customtkinter as ctk
from image_widgets import *
from PIL import Image, ImageTk
from image_processing import *
import numpy as np

from pdf_export import export_pdf


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

        # Place all three page layouts at identical grid coordinates so they overlap and fill the framework space.
        self.page1.grid(row=0,column=0,sticky="nsew")
        self.page2.grid(row=0,column=0,sticky="nsew")
        self.page3.grid(row=0,column=0,sticky="nsew")

        # Invoke external helper layout functions to populate all three functional frames with distinct elements.
        make_page1(self)
        make_page2(self)
        make_page3(self)

        # Initialize tracking instance variables to hold active canvas images and visual crosshair lines.
        self.canvas_image = None
        self.v_line = None
        self.h_line = None

        # Bring the primary image selection frame layer to the absolute front of the display stack on startup.
        self.show_page(self.page1)

        # Initialize the global tracking variable states designed to manage image cropping boundaries safely.
        self.crop_rect = None
        self.is_selecting = False

        # Establish blank anchor coordinates that capture the precise click start location on the viewport canvas.
        self.start_x = None
        self.start_y = None

        # Create a state element placeholder configured to store the clean, sorted bounds coordinates of the crop box.
        self.crop_display_coords = None

        # Bind the enter key release event globally to instantly calculate and render the crop block mosaic view.
        self.bind("<Return>", self.confirm_crop)

    def show_page(self, page):
        # Pull the requested page frame layout to the front of the screen stack to make it visible.
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

        # Extract the live spatial x and y coordinates generated by the mouse tracking motion hardware.
        x, y = event.x, event.y

        # Determine the physical outer bounding coordinates of the compressed photo inside the canvas zone.
        left, top = self.image_x, self.image_y
        right, bottom = (
            left + self.display_width,
            top + self.display_height
        )

        # Hide the crosshair guides completely if the cursor path travels outside active image parameters.
        if not (left <= x <= right and top <= y <= bottom):
            self.hide_crosshair()
            return

        # Toggle the hidden state visibility attribute on both grid lines to reveal them over the rendering.
        for line in (self.v_line, self.h_line):
            self.image_canvas.itemconfigure(
                line,
                state="normal"
            )

        # Re-draw the vertical crosshair column segment using structural coordinates at the cursor site.
        self.image_canvas.coords(
            self.v_line,
            x, top,
            x, bottom
        )

        # Re-draw the horizontal crosshair column segment using structural coordinates at the cursor site.
        self.image_canvas.coords(
            self.h_line,
            left, y,
            right, y
        )

    def hide_crosshair(self, event=None):
        # Cycle through line references to sweep tracking vectors out of sight across the primary viewport.
        for line in (self.v_line, self.h_line):
            if line is not None:
                self.image_canvas.itemconfigure(
                    line,
                    state="hidden"
                )

    def start_crop(self, event):
        # Block layout crop procedures if the initial button click lands outside image spatial dimensions.
        if not (
            self.image_x <= event.x <= self.image_x + self.display_width
            and
            self.image_y <= event.y <= self.image_y + self.display_height
        ):
            return

        # Mark selection states as active and cache baseline click coordinates to establish drawing origins.
        self.is_selecting = True
        self.start_x = event.x
        self.start_y = event.y

        # Evaporate stale box outline drawings from the window frame buffer before plotting the next area.
        if self.crop_rect is not None:
            self.image_canvas.delete(self.crop_rect)

        # Map a brand-new scalable blue rectangle geometry layer onto the workspace using current mouse positions.
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
            # Query the input text controls to dynamically parse comparative mathematical aspect proportions.
            rows = int(self.rows_entry.get())
            cols = int(self.cols_entry.get())

            # Enforce non-zero checks on the dimension integer variables to protect division steps from crashing.
            if rows <= 0 or cols <= 0:
                return None

            # Divide structural grid rows by columns to produce the exact decimal scaling aspect coefficient factor.
            # Image aspect ratio is width / height: columns / rows.
            return cols / rows

        # Handle formatting data conversion anomalies gracefully by returning empty object states to workflows.
        except ValueError:
            return None


    def update_crop(self, event):
        # Abort mouse movement update processes immediately if selection state triggers return false variables.
        if not self.is_selecting:
            return

        # Fetch the active mathematical grid aspect constraint value before scaling bounding vectors.
        ratio = self.get_crop_ratio()

        # Halt bounding box calculation pipelines if current numerical form values cannot resolve to a ratio.
        if ratio is None:
            return

        # Calculate comparative directional distance offsets between modern cursor sites and click origins.
        dx = event.x - self.start_x
        dy = event.y - self.start_y

        # Establish structural alignment multipliers using standard positive and negative step vectors.
        sign_x = 1 if dx >= 0 else -1
        sign_y = 1 if dy >= 0 else -1

        # Strip sign records from distance offsets to determine the raw absolute magnitude values of scaling steps.
        width = abs(dx)
        height = abs(dy)

        # Compare absolute coordinate dimensions against the aspect target value to normalize growth vectors.
        if width / max(height, 1) > ratio:
            height = width / ratio
        else:
            width = height * ratio

        # Project balanced rectangle corner boundaries using structural math offsets mixed with direction maps.
        x = self.start_x + sign_x * width
        y = self.start_y + sign_y * height

        # Clamp horizontal boundary projections to lock the scaling outline squarely inside image canvas dimensions.
        x = min(
            max(x, self.image_x),
            self.image_x + self.display_width
        )

        # Clamp vertical boundary projections to lock the scaling outline squarely inside image canvas dimensions.
        y = min(
            max(y, self.image_y),
            self.image_y + self.display_height
        )

        # Alter the existing coordinate attributes on the active canvas rectangle layout object to update shapes.
        self.image_canvas.coords(
            self.crop_rect,
            self.start_x,
            self.start_y,
            x,
            y
        )


    def finish_crop(self, event):
        # Halt capture sequence steps if mouse release calls fire outside active user selection tracking cycles.
        if not self.is_selecting:
            return

        # Clear selection indicators to signal that the active geometry drawing loop has officially drawn to a close.
        self.is_selecting = False

        # Read the raw coordinate vertices values straight from the finalized structural canvas shape container.
        x1, y1, x2, y2 = self.image_canvas.coords(self.crop_rect)

        # Sort layout measurements logically into uniform structural vectors tracking left, top, right, and bottom.
        self.crop_display_coords = (
            min(x1, x2),
            min(y1, y2),
            max(x1, x2),
            max(y1, y2)
        )


    def confirm_crop(self, event=None):
        # Interrupt confirmation processes immediately if no spatial crop area coordinates have been mapped out.
        if self.crop_display_coords is None:
            return

        # Crop coordinates on the displayed canvas image
        left, top, right, bottom = self.crop_display_coords

        # Determine how much the original image was scaled when it was displayed on the canvas window container.
        scale_x = self.original_image.width / self.display_width
        scale_y = self.original_image.height / self.display_height

        # Convert the raw UI display pixel coordinates cleanly back into real unscaled original image indices.
        x1 = int((left - self.image_x) * scale_x)
        y1 = int((top - self.image_y) * scale_y)
        x2 = int((right - self.image_x) * scale_x)
        y2 = int((bottom - self.image_y) * scale_y)

        # Crop the original image
        self.cropped_image = self.original_image.crop(
            (x1, y1, x2, y2)
        )

        # Permanent untouched copy copy for reference.
        self.original_cropped_image = self.cropped_image.copy()
        self.preview_image = self.cropped_image.copy()

        # Build Rubik palette array structures.
        palette = []

        # Iterate through the entry widgets to extract text string fields and transform them into RGB profiles.
        for _, entry in self.color_widgets:
            try:
                color = entry.get().lstrip("#")

                rgb = [
                    int(color[i:i+2], 16)
                    for i in (0, 2, 4)
                ]

                palette.append(rgb)

            except:
                pass

        # Package the validated color sequence collections neatly into a dedicated operational NumPy array layer.
        palette = np.array(palette, dtype=np.uint8)

        # Persist the processed color reference arrays directly onto the main class frame layout property state.
        self.palette = palette

        # Extract textual information dimensions directly from the input form controls to extract baseline scaling.
        rows = int(self.rows_entry.get())
        cols = int(self.cols_entry.get())

        # Generate initial mosaic graphics views.
        self.processed_image = process_image(
            self.cropped_image,
            palette,
            rows,
            cols
        )

        # Trigger execution loops to map out new visualization frames onto the dual results preview area canvas.
        self.update_page3_images()

        # Elevate page 3 workspace layers to bring filter editing interfaces smoothly into primary visual focus.
        self.show_page(self.page3)


    def fit_image_canvas(self, image, canvas, force_size=None):
        # Force the thread queue to process pending layout dimensions updates to ensure geometric checks are solid.
        canvas.update_idletasks()

        # Retrieve structural boundary heights and widths measurements straight from the active rendering box.
        w = canvas.winfo_width()
        h = canvas.winfo_height()

        # Halt geometry drawing loops completely if baseline canvas width or height measurements read under zero.
        if w <= 1 or h <= 1:
            return

        # Extract intrinsic pixel dimensions mapping coordinates directly from image property memory metrics.
        iw, ih = image.size

        # Formulate uniform proportional scaling multipliers if custom dimensions limits are missing from arguments.
        if force_size is None:
            scale = min(w / iw, h / ih)

            nw = int(iw * scale)
            nh = int(ih * scale)
        else:
            nw, nh = force_size

        # Perform the image transformation workflow using fast nearest neighbor pixel interpolation math structures.
        resized = image.resize(
            (nw, nh),
            Image.Resampling.NEAREST
        )

        # Construct a native Tkinter photo canvas image structural asset containing the newly resized pixel maps.
        tk_img = ImageTk.PhotoImage(resized)

        # Clean old obsolete viewport assets entirely off the layout stack before drawing fresh graphical outputs.
        canvas.delete("all")

        # Re-assign structural properties directly to instance containers to prevent memory garbage sweeps.
        canvas.image_ref = tk_img

        # Render the prepared final graphic content layer squarely centered inside the active backdrop canvas region.
        canvas.create_image(
            (w - nw) // 2,
            (h - nh) // 2,
            anchor="nw",
            image=tk_img
        )


    def update_page3_images(self, event=None):
        # Verify if appropriate image asset slices exist within context fields before calculating drawing bounds.
        if not hasattr(self, "cropped_image"):
            return

        # Signal update task structures to sync frame measurements before applying comparative scale factor math.
        self.crop_canvas.update_idletasks()

        # Pull down current rendering boundaries from the core layout parameters of the left preview frame canvas.
        cw = self.crop_canvas.winfo_width()
        ch = self.crop_canvas.winfo_height()

        # Collect internal asset size metrics to accurately structure parallel comparative panel transformations.
        iw, ih = self.cropped_image.size

        # Determine structural boundary ratios by taking the smaller fraction score between width and height values.
        scale = min(cw / iw, ch / ih)

        # Apply the scalar ratio values to generate perfectly mirrored dimensions limits for both display panels.
        nw = int(iw * scale)
        nh = int(ih * scale)

        # Mount the updated primary source clip graphic layer securely inside the left-hand workspace frame block.
        self.fit_image_canvas(
            self.preview_image,
            self.crop_canvas,
            force_size=(nw, nh)
        )

        # Draw the finished filtered mosaic grid output layer precisely into the right-hand inspection canvas panel.
        self.fit_image_canvas(
            self.processed_image,
            self.process_canvas,
            force_size=(nw, nh)
        )


    def apply_page3_effects(self):
        # Validate that historical crop reference elements are active in system memory variables before computing effects.
        if not hasattr(self, "original_cropped_image"):
            return

        # Fetch numeric row and column values directly from text inputs to verify output structural resolutions.
        rows = int(self.rows_entry.get())
        cols = int(self.cols_entry.get())

        # Execute complex multi-filter pixel modification pipelines on the untouched baseline image clipping data layer.
        self.preview_image = apply_effects(
            self.original_cropped_image,
            brightness=self.brightness_slider.get(),
            contrast=self.contrast_slider.get(),
            saturation=self.saturation_slider.get(),
            sharpness=self.sharpness_slider.get(),
            blur=self.blur_slider.get(),
            flip_horizontal=self.flip_x_switch.get(),
            flip_vertical=self.flip_y_switch.get()
        )

        # Re-run quantization algorithms over the filtered preview image array to output fresh block patterns.
        self.processed_image = process_image(
            self.preview_image,
            self.palette,
            rows,
            cols
        )

        # Evaluate secondary switch states to apply a low-pass blurring pass over the final pixel block matrix.
        if self.blur_mosaic_switch.get():
            self.processed_image = blur_mosaic(
                self.processed_image,
                radius=1
            )

        # Invoke dual display refresh mechanisms to redraw updated graphics panels side-by-side on page 3 view.
        self.update_page3_images()


    def revert_changes(self):
        # Reset all structural image adjustments filters sliders back to baseline un-enhanced configuration weights.
        self.brightness_slider.set(1)
        self.contrast_slider.set(1)
        self.saturation_slider.set(1)
        self.sharpness_slider.set(1)
        self.blur_slider.set(0)

        # Set all independent geometric inversion and overlay canvas blur toggle states back to deactivated rules.
        self.flip_x_switch.deselect()
        self.flip_y_switch.deselect()
        self.blur_mosaic_switch.deselect()

        # Re-run full calculations stacks using the restored defaults to completely wipe temporary display states.
        self.apply_page3_effects()

    def export_current_pdf(self):

        # Guard export threads from fatal logic runtime errors if no quantified mosaic array is verified in state memory.
        if not hasattr(self, "processed_image"):
            return

        # Launch OS native save explorer dialog trees to prompt user file tree targets destination designations.
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[
                ("PDF files", "*.pdf")
            ],
            title="Export PDF"
        )

        # Interrupt document execution workflows immediately if the output destination data path evaluates to blank.
        if not filepath:
            return

        # Print current resolution measurements directly to the system diagnostic outputs console for validation.
        # Invoke downstream assembly modules to translate raw matrix outputs into structured multi-page PDF assets.
        pages = export_pdf(
            self.processed_image
        )

        # Compile individual extracted PIL canvas frames into a single, cohesive, flattened electronic PDF structure document.
        pages[0].save(
            filepath,
            save_all=True,
            append_images=pages[1:],
            format="PDF",
            resolution=100
        )

app = App()
app.mainloop()
