import customtkinter as ctk

def make_page1(app):
    # Build all widgets belonging to page 1
    p1_open_button(app)
    
def make_page2(app):

    # Page 2 Layout:
    # ┌──────────────────────────┐
    # │        Top Bar           │
    # ├──────────┬───────────────┤
    # │ Left     │               │
    # │ Panel    │  Image Panel  │
    # │          │               │
    # └──────────┴───────────────┘

    # app.page2.bind("<Configure>", app.update_image) # shifted it here to make it organised

    app.page2.grid_rowconfigure(0, weight=1)   # top bar
    app.page2.grid_rowconfigure(1, weight=12)  # main content area gets most of the space

    app.page2.grid_columnconfigure(0, weight=1)

    p2_topbar(app)
    p2_main_area(app)

    p2_image_display(app)

def p2_topbar(app):

    # Fixed-height navigation/control area at the top
    app.topbar = ctk.CTkFrame(
        app.page2,
        height=50,
        fg_color="red"
    )

    app.topbar.grid(
        row=0,
        column=0,
        sticky="ew"
    )

    # Prevent child widgets from changing the bar's height
    app.topbar.grid_propagate(False)

def p2_main_area(app):

    # Main workspace containing the sidebar and image viewer
    app.main_area = ctk.CTkFrame(
        app.page2,
        fg_color="yellow",
    )

    app.main_area.grid(   #created main_area as 0th col and 1st row of page2 Frame
        row=1,
        column=0,
        sticky="nsew"
    )

    # Split main_area into two columns: sidebar + image area
    app.main_area.grid_rowconfigure(0, weight=1)

    app.main_area.grid_columnconfigure(0, weight=2)
    app.main_area.grid_columnconfigure(1, weight=10)

    p2_left_panel(app)
    p2_image_display(app)

def p2_left_panel(app):

    # Sidebar reserved for tools, controls, and future options
    app.left_panel = ctk.CTkFrame(
        app.main_area,
        width=250,
        fg_color="blue"
    )

    app.left_panel.grid(   #left_panel is frame at position 0,0 of the grid of main_area
        row=0,
        column=0,
        sticky="nsew"
    )

    # Keep the sidebar width fixed
    app.left_panel.grid_propagate(False)

def p2_image_display(app):

    # Main panel where the loaded image will be displayed
    app.image_panel = ctk.CTkFrame(app.main_area, fg_color="green")

    app.image_panel.grid(  #image_panel is frame at position 0,1 of the grid of main_area
        row=0,
        column=1,
        sticky="nsew",
    )

    # Center the image label within the image panel
    app.image_panel.grid_rowconfigure(0, weight=1)
    app.image_panel.grid_columnconfigure(0, weight=1)

    app.image_label = ctk.CTkLabel(
        app.image_panel,
        text="No Image"
    )

    app.image_label.grid(row=0, column=0, sticky="nsew")

    # Resize the displayed image whenever the image panel size changes
    app.image_panel.bind("<Configure>", app.update_image)

def p1_open_button(app):

    # Keep the button centered on page 1
    app.page1.grid_rowconfigure(0, weight=1)
    app.page1.grid_columnconfigure(0, weight=1)

    app.button = ctk.CTkButton(
        app.page1,
        text="Open Image",
        width=100,
        height=28,
        command=app.open_image
    )

    app.button.grid(row=0, column=0)