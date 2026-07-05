# solution.py

# part a: theory
# 1. weight parameter tells the grid manager how to distribute extra space when the window resizes. weight=1 means it expands proportionally. kinda like reallocating a dynamic array based on terminal size.
# 2. sticky="nsew" makes the widget stretch north south east west to completely fill its grid cell. if you leave it out, it just sits in the center and wastes space.
# 3. stacking is just the z-order of how widgets are drawn. tkraise() brings a specific frame to the top of the stack. think of it like moving a node to the head of a linked list so it renders first/on top.

import customtkinter as ctk

# setting up the main window. no manual malloc needed for the window buffer
app = ctk.CTk()
app.geometry("400x400")
app.title("Q1 Grid Layout")

# part b: configuring the grid to scale equally
# setting weight=1 for a 2x2 grid so all 4 quadrants stretch when maximized
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

# allocating 4 frames with different colors and sticking them to the grid
# quadrant 1 (top left)
frame1 = ctk.CTkFrame(app, fg_color="#FF5555", corner_radius=0)
frame1.grid(row=0, column=0, sticky="nsew")

# quadrant 2 (top right)
frame2 = ctk.CTkFrame(app, fg_color="#5555FF", corner_radius=0)
frame2.grid(row=0, column=1, sticky="nsew")

# quadrant 3 (bottom left)
frame3 = ctk.CTkFrame(app, fg_color="#55FF55", corner_radius=0)
frame3.grid(row=1, column=0, sticky="nsew")

# quadrant 4 (bottom right)
frame4 = ctk.CTkFrame(app, fg_color="#FFFF55", corner_radius=0)
frame4.grid(row=1, column=1, sticky="nsew")

# run the event loop
app.mainloop()