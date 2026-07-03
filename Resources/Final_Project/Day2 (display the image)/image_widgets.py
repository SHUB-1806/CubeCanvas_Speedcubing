import customtkinter as ctk

def p1_open_button(app):

    # Allow widgets on page 1 to stay centered and resize properly
    app.page1.grid_rowconfigure(0, weight=1)
    app.page1.grid_columnconfigure(0, weight=1)

    # Create a button that opens the file explorer when clicked
    app.button = ctk.CTkButton(
        app.page1,
        text="Open Image",
        width=100,
        height=28,
        command=app.open_image  # Calls the image selection function on button click
    )

    # Position the button at the center of page 1
    app.button.grid(row=0, column=0)

def p2_image_display(app):

    # Allow the image display area to expand with the window size
    app.page2.grid_rowconfigure(0, weight=1)
    app.page2.grid_columnconfigure(0, weight=1)

    # Create a label that will later hold the selected image
    app.image_label = ctk.CTkLabel(   #creating the empty space for image to be displayed on page2
        app.page2,
        text="No Image"  # Placeholder text shown before any image is loaded
    )

    # Place the image label at the center of page 2
    app.image_label.grid(row=0, column=0)   #deciding where it will be located