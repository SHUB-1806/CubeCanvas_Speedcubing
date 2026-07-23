'''
1. Event binding is a way to link a user interaction or a system event with a python function, such that the python function is automatically executed when the event is triggered.
2. The button's command fires only after a full mouse click on the button while the bind fires as soon as the user releases any keyboard key while hovering over that widget.
3. When we store a function as function(), the function is called immediately while when storing as function, the function is pointed to and is executed when another piece of code runs it, like an event binding.
4. A lambda function is a small function that is defined without a name. We use it to pass a function reference when having to pass variables in our command in the binding or button command.
'''

import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Question 2")
        self.geometry("1000x600")

        self.entry = ctk.CTkEntry(self, width = 100)
        self.entry.pack()

        self.label = ctk.CTkLabel(self, text="Character count: 0")
        self.label.pack()

        self.entry.bind("<KeyRelease>", self.update_count)

    def update_count(self, event):
        text = self.entry.get()
        count = len(text)
        self.label.configure(text=f"Character count: {count}")

app = App()
app.mainloop()