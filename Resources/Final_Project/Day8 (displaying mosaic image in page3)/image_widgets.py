import customtkinter as ctk
import tkinter as tk


# ==========================================================
# PAGE CREATION
# ==========================================================

def make_page1(app):
    """Create widgets for the opening page."""
    p1_open_button(app)


def make_page2(app):
    """Configure and build the image editing page."""

    # Top bar + main content area
    app.page2.grid_rowconfigure(0, weight=1)
    app.page2.grid_rowconfigure(1, weight=12)

    app.page2.grid_columnconfigure(0, weight=1)

    p2_topbar(app)
    p2_main_area(app)


def make_page3(app):
    """Configure and build the preview page."""

    # Top bar + preview area
    app.page3.grid_rowconfigure(0, weight=1)
    app.page3.grid_rowconfigure(1, weight=12)

    app.page3.grid_columnconfigure(0, weight=1)

    p3_topbar(app)
    p3_main_area(app)


# ==========================================================
# PAGE 3 : TOP BAR
# ==========================================================

def p3_topbar(app):
    """
    Top navigation bar for the preview page.

    Contains:
    - Page title
    - Back button
    - Close button
    """

    # Initialize a structural frame context on page 3 that serves as the placeholder for preview navigation tools.
    app.p3_topbar = ctk.CTkFrame(app.page3)

    app.p3_topbar.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=5,
        pady=5
    )

    app.p3_topbar.grid_rowconfigure(0, weight=1)

    #
    # Layout:
    #
    # [Title][ ][ ][ ][ ][←][✕]
    #
    for i in range(5):
        app.p3_topbar.grid_columnconfigure(i, weight=0)

    # Spacer column
    app.p3_topbar.grid_columnconfigure(5, weight=1)

    app.p3_topbar.grid_columnconfigure(6, weight=0)

    # Page title
    ctk.CTkLabel(
        app.p3_topbar,
        text="Preview"
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=10
    )

    # Return to crop page
    ctk.CTkButton(
        app.p3_topbar,
        text="←",
        width=30,
        command=lambda: app.show_page(app.page2)
    ).grid(
        row=0,
        column=5,
        sticky="e",
        padx=10
    )

    # Return to home page
    ctk.CTkButton(
        app.p3_topbar,
        text="✕",
        width=30,
        command=lambda: app.show_page(app.page1)
    ).grid(
        row=0,
        column=6,
        padx=(10, 15)
    )


# ==========================================================
# PAGE 3 : MAIN AREA
# ==========================================================

def p3_main_area(app):
    """
    Main content area of the preview page.

    Layout:

    ┌──────────┬─────────────────────┐
    │ Left     │ Image Preview Area  │
    │ Panel    │                     │
    └──────────┴─────────────────────┘
    """

    # Establish the main lower content panel frame context layer sitting right beneath the page 3 title section.
    app.p3_main = ctk.CTkFrame(app.page3)

    app.p3_main.grid(
        row=1,
        column=0,
        sticky="nsew"
    )

    app.p3_main.grid_rowconfigure(0, weight=1)

    # Left panel : image display ratio = 2 : 10
    app.p3_main.grid_columnconfigure(0, weight=2)
    app.p3_main.grid_columnconfigure(1, weight=10)

    p3_left_panel(app)
    p3_image_display(app)


# ==========================================================
# PAGE 3 : LEFT PANEL
# ==========================================================

def p3_left_panel(app):
    """
    Sidebar for future controls.

    Currently contains only a title.
    """

    # Instantiate a standalone modular dashboard side menu container frame nested inside the page 3 workspace base.
    app.p3_left = ctk.CTkFrame(app.p3_main)

    app.p3_left.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=5,
        pady=5
    )

    app.p3_left.grid_rowconfigure(0, weight=1)
    app.p3_left.grid_columnconfigure(0, weight=1)

    ctk.CTkLabel(
        app.p3_left,
        text="Processed Preview"
    ).grid(
        row=0,
        column=0,
        pady=20
    )


# ==========================================================
# PAGE 3 : IMAGE DISPLAY AREA
# ==========================================================

def p3_image_display(app):
    """
    Display the original crop and the processed mosaic.

    Layout:

    ┌─────────────────┬─────────────────┐
    │ Cropped Image   │ Processed Image │
    └─────────────────┴─────────────────┘
    """

    # Assemble a comprehensive dual-column image viewing canvas container centered inside the main page 3 module.
    app.p3_image_panel = ctk.CTkFrame(app.p3_main)

    app.p3_image_panel.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=5,
        pady=5
    )

    app.p3_image_panel.grid_rowconfigure(0, weight=1)

    # Two equally sized preview canvases
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

    app.crop_canvas.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=5,
        pady=5
    )

    app.process_canvas.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=5,
        pady=5
    )

    #
    # Redraw images whenever the canvases resize
    #
    app.crop_canvas.bind(
        "<Configure>",
        app.update_page3_images
    )

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
