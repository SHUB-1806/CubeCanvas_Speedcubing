'''
THEORY

1)Event binding in Tkinter is the process of connecting a user event liking pressing a key to a function. When 
  that event happens Tkinter automatically executes the associated function.

2)Although both are used to execute function but they work differently, the command parameter is mainly used
  with buttons and executes a fuction only when the button is clicked wheras the.bind() method is used to connect various
  events such askey presses ,key releasse or mouse clicks to a function,thus the function is executed whenever this specific
 events are occured and not just clicking the button.

3)Writing a function passes the function itself to Tkinter without executing it. Tkinter calls it later when the required
  event as occured. On the other hand writing function() executes the function immediately while the program iss running 
  which is not usually desired when we assign commands to buttons or events.

4)Lambada is used to create a temporary function that delays the immediate execution of a function and ensure 
  that when the argument that has passed will run only when specific events occurs like pressing or releasing a key.
  In short , lambada assign a function arguement to a specific event or button.#
'''
import customtkinter as ctk
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Character Counter")
        self.geometry("1000x600")
        self.entry= ctk.CTkEntry(self)
        self.entry.pack(pady=20)
        self.label = ctk.CTkLabel( self,text= "Charcter Count : 0")
        self.label.pack()
        self.entry.bind("<KeyRelease>", self.update_count)

    def update_count(self,event):
         count = len(self.entry.get())
         self.label.configure(text=f"Character Count: {count}")

        
app = App()
app.mainloop()
