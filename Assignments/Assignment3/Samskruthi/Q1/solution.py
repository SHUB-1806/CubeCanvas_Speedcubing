# Theory Questions:
# 1. The weight parameter determines how extra space is distributed to rows and columns when the window is resized. A row or column with a higher weight expands more than one with a lower weight.
# 2. The sticky="nsew" argument makes the widget stick to the North, South, East, and West sides of its grid cell. This allows the widget to stretch and fill the entire available space.
# 3. Stacking frames means placing multiple frames in the same position, with only one visible at a time. The tkraise() method brings the selected frame to the front, making it the visible page while hiding the others.
# Coding :
import customtkinter as ctk

# Create the main window
app = ctk.CTk()
app.title("2 x 2 Grid")
app.geometry("400x400")

# Configure the grid (2 rows × 2 columns)
app.grid_rowconfigure((0, 1), weight=1)
app.grid_columnconfigure((0, 1), weight=1)

# Create four colored frames
frame1 = ctk.CTkFrame(app, fg_color="red")
frame2 = ctk.CTkFrame(app, fg_color="blue")
frame3 = ctk.CTkFrame(app, fg_color="green")
frame4 = ctk.CTkFrame(app, fg_color="yellow")

# Place the frames in the grid
frame1.grid(row=0, column=0, sticky="nsew")
frame2.grid(row=0, column=1, sticky="nsew")
frame3.grid(row=1, column=0, sticky="nsew")
frame4.grid(row=1, column=1, sticky="nsew")

# Start the application
app.mainloop()

