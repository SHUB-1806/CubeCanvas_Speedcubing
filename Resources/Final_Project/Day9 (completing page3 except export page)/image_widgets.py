import customtkinter as ctk
import tkinter as tk


def make_page1(app):
    # Initialize page 1 layout configurations by calling the helper function to construct the entry button widget.
    p1_open_button(app)


def make_page2(app):
    # Partition page 2 vertically into two distinct sections, allocating structural room for a top bar and main content area.
    app.page2.grid_rowconfigure(0, weight=1)
    app.page2.grid_rowconfigure(1, weight=12)

    # Force the lone layout column configuration on page 2 to expand seamlessly across the entire window framework width.
    app.page2.grid_columnconfigure(0, weight=1)

    # Instantiate the global persistent configuration frames that populate the layout sections of page 2 view space.
    p2_topbar(app)
    p2_main_area(app)


def make_page3(app):
    # Partition page 3 vertically into two distinct sections, allocating structural room for a top bar and main content area.
    app.page3.grid_rowconfigure(0, weight=1)
    app.page3.grid_rowconfigure(1, weight=12)

    # Force the lone layout column configuration on page 3 to expand seamlessly across the entire window framework width.
    app.page3.grid_columnconfigure(0, weight=1)

    # Instantiate the global persistent configuration frames that populate the layout sections of page 3 view space.
    p3_topbar(app)
    p3_main_area(app)

def p3_topbar(app):
    """
    Build the top navigation bar for Page 3.

    The topbar contains:
    - Export button
    - Back button (returns to Page 2)
    - Close button (returns to Page 1)

    Layout:

    Export                    ←    ✕
    """

    #
    # Container for topbar widgets
    #
    app.p3_topbar = ctk.CTkFrame(app.page3)

    app.p3_topbar.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=5,
        pady=5
    )

    #
    # Allow the row to expand vertically
    #
    app.p3_topbar.grid_rowconfigure(0, weight=1)

    #
    # Column layout:
    #
    # [Export][Spacer][Back][Close]
    #
    # Spacer consumes all extra horizontal space,
    # pushing the navigation buttons to the right.
    #
    app.p3_topbar.grid_columnconfigure(0, weight=0)
    app.p3_topbar.grid_columnconfigure(1, weight=1)
    app.p3_topbar.grid_columnconfigure(2, weight=0)
    app.p3_topbar.grid_columnconfigure(3, weight=0)

    #
    # Export button
    #
    # Used to save the generated Rubik mosaic.
    # Export functionality can be added later.
    #
    app.export_button = ctk.CTkButton(
        app.p3_topbar,
        text="Export"
    )

    app.export_button.grid(
        row=0,
        column=0,
        padx=(10, 5),
        pady=10,
        sticky="w"
    )

    #
    # Back button
    #
    # Returns to the crop/settings page
    # while preserving the current work.
    #
    ctk.CTkButton(
        app.p3_topbar,
        text="←",
        width=30,
        command=lambda: app.show_page(app.page2)
    ).grid(
        row=0,
        column=2,
        padx=10,
        pady=10
    )

    #
    # Close button
    #
    # Returns to the home page.
    # Depending on implementation, this may
    # discard the current project.
    #
    ctk.CTkButton(
        app.p3_topbar,
        text="✕",
        width=30,
        command=lambda: app.show_page(app.page1)
    ).grid(
        row=0,
        column=3,
        padx=(5, 15),
        pady=10
    )

def p3_main_area(app):
    # Create the core workflow interface staging base module nested safely within the page 3 primary canvas architecture.
    app.p3_main = ctk.CTkFrame(app.page3)

    app.p3_main.grid(
        row=1,
        column=0,
        sticky="nsew"
    )

    # Stretch the vertical column dimensions across the inner content frame to occupy all leftover preview space.
    app.p3_main.grid_rowconfigure(0, weight=1)

    # Apportion the active workspace unevenly between an aggregate sidebar column and a wider dual preview image column.
    app.p3_main.grid_columnconfigure(0, weight=3)
    app.p3_main.grid_columnconfigure(1, weight=9)

    # Call external grid mapping sequences to construct the slider effect sidebar and the twin preview canvas layouts.
    p3_left_panel(app)
    p3_image_display(app)

def p3_left_panel(app):
    """
    Build the left sidebar of Page 3.

    The sidebar contains:
    - Image effect controls
    - Toggle switches
    - Revert button

    A scrollable frame is used so that additional
    controls can be added in the future without
    overflowing the window.
    """

    #
    # Scrollable container for all Page 3 controls
    #
    app.p3_left = ctk.CTkScrollableFrame(app.p3_main)

    app.p3_left.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=5,
        pady=5
    )

    # Force the lone layout column configuration on page 3 sidebar to stretch seamlessly across the container framework width.
    app.p3_left.grid_columnconfigure(0, weight=1)

    #
    # Sidebar title
    #
    ctk.CTkLabel(
        app.p3_left,
        text="IMAGE EFFECTS",
        font=("Arial", 24, "bold")
    ).pack(
        pady=(25, 20)
    )

    #
    # Slider configuration:
    #
    # (Label text,
    #  attribute name used to save the slider,
    #  minimum value,
    #  maximum value,
    #  default value)
    #
    slider_configs = [
        ("Brightness", "brightness_slider", 0, 2, 1),
        ("Contrast", "contrast_slider", 0, 2, 1),
        ("Saturation", "saturation_slider", 0, 2, 1),
        ("Sharpness", "sharpness_slider", 0, 3, 1),
        ("Blur", "blur_slider", 0, 5, 0),
    ]

    #
    # Create all effect sliders
    #
    for text, attr_name, min_val, max_val, default in slider_configs:

        #
        # Frame containing a label and its slider
        #
        frame = ctk.CTkFrame(app.p3_left)

        frame.pack(
            fill="x",
            padx=8,
            pady=4
        )

        #
        # Slider label
        #
        ctk.CTkLabel(
            frame,
            text=text
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 8)
        )

        #
        # Effect slider
        #
        slider = ctk.CTkSlider(
            frame,
            from_=min_val,
            to=max_val,

            # Regenerate previews whenever
            # the slider value changes
            command=lambda value: app.apply_page3_effects()
        )

        #
        # Set default slider position
        #
        slider.set(default)

        slider.pack(
            fill="x",
            padx=15,
            pady=(0, 10)
        )

        #
        # Save the slider as an attribute
        #
        # Example:
        # app.brightness_slider
        # app.contrast_slider
        #
        setattr(app, attr_name, slider)

    #
    # Switch section
    #
    switch_frame = ctk.CTkFrame(app.p3_left)

    switch_frame.pack(
        fill="x",
        padx=10,
        pady=10
    )

    #
    # Horizontal flip toggle
    #
    app.flip_x_switch = ctk.CTkSwitch(
        switch_frame,
        text="Flip X",
        command=app.apply_page3_effects
    )

    app.flip_x_switch.pack(
        anchor="w",
        padx=15,
        pady=(15, 10)
    )

    #
    # Vertical flip toggle
    #
    app.flip_y_switch = ctk.CTkSwitch(
        switch_frame,
        text="Flip Y",
        command=app.apply_page3_effects
    )

    app.flip_y_switch.pack(
        anchor="w",
        padx=15,
        pady=10
    )

    #
    # Optional blur applied to the
    # final Rubik mosaic
    #
    app.blur_mosaic_switch = ctk.CTkSwitch(
        switch_frame,
        text="Blur Mosaic",
        command=app.apply_page3_effects
    )

    app.blur_mosaic_switch.pack(
        anchor="w",
        padx=15,
        pady=(10, 15)
    )

    #
    # Restore all controls to their
    # default values
    #
    app.revert_button = ctk.CTkButton(
        app.p3_left,
        text="Revert Changes",
        command=app.revert_changes
    )

    app.revert_button.pack(
        fill="x",
        padx=10,
        pady=(0, 15),
        side="bottom"
    )

def p3_image_display(app):
    # Establish a spacious dual preview framing panel inside the page 3 dashboard area to mount comparison graphics output.
    app.p3_image_panel = ctk.CTkFrame(app.p3_main)

    app.p3_image_panel.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=5,
        pady=5
    )

    # Ensure dynamic resizing instructions propagate fully across the designated internal framework grid row structures.
    app.p3_image_panel.grid_rowconfigure(0, weight=1)

    # Apportion the horizontal panel space evenly between the original edited crop preview and the final mosaic display canvas.
    app.p3_image_panel.grid_columnconfigure(0, weight=1)
    app.p3_image_panel.grid_columnconfigure(1, weight=1)

    #
    # Canvas showing cropped image
    #
    app.crop_canvas = tk.Canvas(
        app.p3_image_panel,
        bg="#242424",
        highlightthickness=0,
        bd=0
    )

    #
    # Canvas showing processed Rubik mosaic
    #
    app.process_canvas = tk.Canvas(
        app.p3_image_panel,
        bg="#242424",
        highlightthickness=0,
        bd=0
    )

    # Anchor the clean cropped photo canvas into the left-hand column position of the preview display dashboard frame.
    app.crop_canvas.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=5,
        pady=5
    )

    # Anchor the rendered mosaic grid canvas into the right-hand column position of the preview display dashboard frame.
    app.process_canvas.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=5,
        pady=5
    )

    # Connect internal canvas resizing instructions directly to the page 3 image display script using configure event hooks.
    app.crop_canvas.bind(
        "<Configure>",
        app.update_page3_images
    )

    # Connect structural mosaic container resizing signals directly to the side by side layout sync re-rendering handler script.
    app.process_canvas.bind(
        "<Configure>",
        app.update_page3_images
    )


def p2_topbar(app):
    # Initialize a clean functional sub-frame inside the parent page 2 layer to house the system monitoring tools.
    app.topbar = ctk.CTkFrame(app.page2)

    app.topbar.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=5,
        pady=5
    )

    app.topbar.grid_rowconfigure(0, weight=1)

    for i in range(5):
        app.topbar.grid_columnconfigure(i, weight=0)

    app.topbar.grid_columnconfigure(5, weight=1)
    app.topbar.grid_columnconfigure(6, weight=0)

    ctk.CTkLabel(
        app.topbar,
        text="Rows"
    ).grid(
        row=0,
        column=0,
        padx=(10, 5),
        pady=10
    )

    app.rows_entry = ctk.CTkEntry(
        app.topbar,
        width=50,
        placeholder_text="0"
    )

    app.rows_entry.grid(
        row=0,
        column=1,
        padx=(0, 10),
        pady=10
    )

    ctk.CTkLabel(
        app.topbar,
        text="×   Columns"
    ).grid(
        row=0,
        column=2,
        pady=10
    )

    app.cols_entry = ctk.CTkEntry(
        app.topbar,
        width=50,
        placeholder_text="0"
    )

    app.cols_entry.grid(
        row=0,
        column=3,
        padx=(5, 10),
        pady=10
    )

    app.total_label = ctk.CTkLabel(
        app.topbar,
        text="=    0 Cubes"
    )

    app.total_label.grid(
        row=0,
        column=4,
        padx=10,
        pady=10
    )

    app.close_button = ctk.CTkButton(
        app.topbar,
        text="✕",
        width=30,
        command=lambda: app.show_page(app.page1)
    )

    app.close_button.grid(
        row=0,
        column=6,
        padx=(10, 15),
        pady=5,
        sticky="e"
    )

    for entry in (app.rows_entry, app.cols_entry):
        entry.bind("<KeyRelease>", app.update_cube_count)

def p2_main_area(app):
    # Create the core workflow interface staging base module nested safely within the page 2 primary canvas architecture.
    app.main_area = ctk.CTkFrame(app.page2)

    app.main_area.grid(
        row=1,
        column=0,
        sticky="nsew"
    )

    app.main_area.grid_rowconfigure(0, weight=1)

    app.main_area.grid_columnconfigure(0, weight=2)
    app.main_area.grid_columnconfigure(1, weight=10)

    p2_left_panel(app)
    p2_image_display(app)


def p2_left_panel(app):
    # Establish an expansive structural configuration side container whose dimensions expand dynamically with the workspace.
    app.left_panel = ctk.CTkFrame(app.main_area)

    app.left_panel.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    app.left_panel.grid_columnconfigure(0, weight=1)
    app.left_panel.grid_columnconfigure(1, weight=2)

    for i in range(6):
        app.left_panel.grid_rowconfigure(i, weight=1)

    p2_cube_colors(app)


def p2_cube_colors(app):
    # Define a static reference registry containing default hex-color string definitions for standard pixel mapping operations.
    default_colors = [
        "#FFFFFF",
        "#FFD500",
        "#009B48",
        "#0046AD",
        "#B71234",
        "#FF5800"
    ]

    app.color_widgets = []

    for row, color in enumerate(default_colors):
        color_box = ctk.CTkFrame(
            app.left_panel,
            width=25,
            height=25,
            fg_color=color,
            corner_radius=5
        )

        color_box.grid_propagate(False)

        color_box.grid(
            row=row,
            column=0,
            padx=(10, 5),
            pady=10
        )

        entry = ctk.CTkEntry(
            app.left_panel,
            width=80
        )

        entry.insert(0, color)

        entry.grid(
            row=row,
            column=1,
            padx=10,
            pady=10,
            sticky="ew"
        )

        entry.bind(
            "<KeyRelease>",
            lambda event, box=color_box, ent=entry:
                update_color_box(box, ent)
        )

        app.color_widgets.append((color_box, entry))


def update_color_box(color_box, entry):
    # Capture the string characters populated within the specific input form field to isolate hex definition modifications.
    color = entry.get()
    # print(color)

    try:
        color_box.configure(fg_color=color)
    except:
        pass


def p2_image_display(app):
    # Force the visual output display layers to stretch continuously to grab all remaining horizontal and vertical coordinates.
    app.image_panel = ctk.CTkFrame(app.main_area)

    app.image_panel.grid(
        row=0,
        column=1,
        sticky="nsew"
    )

    app.image_panel.grid_rowconfigure(0, weight=1)
    app.image_panel.grid_columnconfigure(0, weight=1)

    app.image_canvas = tk.Canvas(
        app.image_panel,
        highlightthickness=0,
        bd=0,
        bg="#2B2B2B",
        cursor="crosshair"
    )

    app.image_canvas.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    

    app.image_canvas.bind("<Motion>", app.move_crosshair)
    app.image_canvas.bind("<Leave>", app.hide_crosshair)

    app.image_canvas.bind("<Button-1>", app.start_crop)

    app.image_canvas.bind("<B1-Motion>",app.update_crop)
    app.image_canvas.bind("<B1-Motion>", app.move_crosshair, add="+")  #without this + it will get confused between initial binding for move_CROSSHAIR

    app.image_canvas.bind("<ButtonRelease-1>", app.finish_crop)

    app.image_panel.bind("<Configure>", app.update_image)


def p1_open_button(app):
    # Balance the parent view space layout grids on page 1 so that nested elements sit perfectly centered in execution.
    app.page1.grid_rowconfigure(0, weight=1)
    app.page1.grid_columnconfigure(0, weight=1)

    app.button = ctk.CTkButton(
        app.page1,
        text="Open Image",
        width=100,
        height=28,
        command=app.open_image
    )

    app.button.grid(
        row=0,
        column=0
    )
