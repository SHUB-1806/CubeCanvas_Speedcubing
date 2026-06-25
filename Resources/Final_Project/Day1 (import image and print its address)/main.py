# to create venv enter: python -m venv myvenv
# to activate venv just type that file in terminal (for bat its .bat and for PowerShell its with .ps)
# if anything went wrong just type exit in terminal that will kill the terminal, then start from start
# also check the python environment selected (bottom right) is same as that of venv (it will still run but the yellow wiggle will not go)

# pip install customtkinter
import tkinter as tk #for all the logic
import customtkinter as ctk #for beatiful UI
from image_widgets import *

class App(ctk.CTk):   #this App class will be a window inherited from class CTk
    def __init__(self):
        super().__init__()  #it calls the parents constructor which is necessary as we are making window through a parent

        self.title("CubeCanvas")   #name of the window
        self.geometry("1000x600")
        self.minsize(800, 500)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill ="both", expand = True)   #window is in a main_frame which expands on complete window

        make_button(self)

    def open_image(self):
        filepath = tk.filedialog.askopenfilename()
        print(filepath)


app = App()
app.mainloop()