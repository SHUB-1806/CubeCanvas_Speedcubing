# PART A
# 1.The purpose of the weight parameter is to ensure that selected regions expand and absorb space when we resize the window. 
#   For example when we choose a grid box (r=0,c=0) and give it a "weight 0" and place a button in this box, when we resize the 
#   window the button's position remains unchanged. But if we give it a "weight 1", the grid box expands as we resize the window 
#   and the button snaps to the center of the box.
# 2.The argument sticky="nsew" ensures that widget placed streches in all the four directions and fits the window.
# 3.Stacking happens when multiple independent container frames are placed into the exact same grid position (row=0, column=0), layering 
#   them directly on top of each other. The tkraise() method is used to manage visibility, for example calling it on a specific frame pulls that 
#   frame to the very top of the stack, hiding all other pages beneath it.


# PART B
import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Q1 Part B")
        self.geometry("400x400")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.q1 = ctk.CTkFrame(self, fg_color="red")
        self.q2 = ctk.CTkFrame(self, fg_color="blue")
        self.q3 = ctk.CTkFrame(self, fg_color="yellow") 
        self.q4 = ctk.CTkFrame(self, fg_color="green")
        
        self.q1.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
        self.q2.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
        self.q3.grid(row=1, column=0, sticky="nsew", padx=2, pady=2)
        self.q4.grid(row=1, column=1, sticky="nsew", padx=2, pady=2)


app =App()
app.mainloop()