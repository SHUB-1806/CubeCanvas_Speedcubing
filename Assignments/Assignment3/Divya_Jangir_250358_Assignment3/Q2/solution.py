# 1. Event binding in Tkinter:
# It connects a user action (like a key press or mouse click) to a function so that the function runs when the event occurs.

# 2. Difference between command and .bind(): command runs a function when a button is clicked.
# .bind("<KeyRelease>", function) runs a function whenever the specified event (here, releasing a key) occurs and passes an event object.

# 3. Difference between function() and function: function() calls the function immediately. function passes the function reference so it runs later when the event occurs.

# 4. Lambda is used to pass arguments to a function or execute multiple statements when assigning commands or bindings.

import customtkinter as ctk

app = ctk.CTk()
app.title("Question 2")
app.geometry("400*200")

entry = ctk.CTkEntry(app, width=300)
entry.pack(pady=20)

label = ctk.CTkLabel(app, text="Character Count: 0")
label.pack()

def update_count(event):
    text = entry.get()
    label.configure(text=f"Character Count: {len(text)}")

entry.bind("<KeyRelease>", update_count)

app.mainloop()