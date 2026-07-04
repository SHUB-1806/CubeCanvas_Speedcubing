import customtkinter as ctk

def make_button(app):

    # making a grid for button
    app.main_frame.grid_rowconfigure(0, weight = 1)
    app.main_frame.grid_columnconfigure(0, weight = 1)

    app.button = ctk.CTkButton(app.main_frame,
                               text = "Open Image",
                               width = 100,
                               height= 28,
                            #    command = app.open_image() #this one calls the function immediately, we dont want that
                               command = app.open_image # this one stores the function (this function is in main.py)
                               
                               ) #created button in main_frame of the window

    app.button.grid(row = 0, column = 0)  #positioned at centre of grid

