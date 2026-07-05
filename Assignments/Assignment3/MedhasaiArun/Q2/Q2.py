# PART A
# 1. An event binding is a mechanism that links a specific user action (mouse click/key press/window resize) to a specific Python function.
#  When that specific action happens, Tkinter automatically fires the linked function. In CubeCanvas for example, event binding is used to make 
#  grid inputs highly responsive. 
# 2. Command acts as a trigger for buttons. When we click on a button, a function is triggered. However, in case of bind, data is sent 
#   continuously containing exact details (like mouse pixel coordinates or which keyboard key was pressed).
# 3. When it is function(), we are asking the function to run immediately when the program starts. Whereas, we use just function in command 
# when we want to run the function only upon clicking the button.
# 4. We sometimes need lamda functions in commands and buttons to delay execution.



import customtkinter as ctk


class ChCounterApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Character Counter")
        self.geometry("400x300")

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True)

        self.entry_box = ctk.CTkEntry(self.container, width=250, height=30, placeholder_text="Type here")
        self.entry_box.pack(pady=(0, 10))  
        self.entry_box.bind("<KeyRelease>", self.update_count)

        self.label = ctk.CTkLabel(self.container, text="Character Count: 0")
        self.label.pack()

    def update_count(self, event):
        current_text = self.entry_box.get()
        self.label.configure( text="Character Count: " + str(len(current_text)))   


app = ChCounterApp()
app.mainloop()
