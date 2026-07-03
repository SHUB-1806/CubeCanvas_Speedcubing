import customtkinter as ctk

def p1_open_button(app):

    # Allow the button to remain centered even when the window is resized
    app.page1.grid_rowconfigure(0, weight=1)
    app.page1.grid_columnconfigure(0, weight=1)

    # Create the button that starts the image selection process
    app.button = ctk.CTkButton(
        app.page1,
        text="Open Image",
        width=100,
        height=28,
        command=app.open_image  # Opens the file picker and loads the selected image
    )

    # Place the button at the center of page 1
    app.button.grid(row=0, column=0)


def p2_image_display(app):

    # Allow the image display area to resize along with the window
    app.page2.grid_rowconfigure(0, weight=1)
    app.page2.grid_columnconfigure(0, weight=1)

    # Create a placeholder label that will later hold the selected image
    app.image_label = ctk.CTkLabel(
        app.page2,
        text="No Image"
    )

    # Position the image label at the center of page 2
    app.image_label.grid(row=0, column=0)