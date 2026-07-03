# Theory Question

# 1. An event binding connects a user action (like a key press or mouse click) to a function. When the event occurs, the function is executed automatically using the .bind() method.
# 2. command runs a function only when a button is clicked. .bind() runs a function when a specific event (such as a key release or mouse click) occurs and passes event information to the function.
# 3. function passes the function so it runs later when the button is clicked. function() calls the function immediately when the program starts.
# 4. A lambda function is used to pass arguments to another function without calling it immediately. It delays the function call until the event happens.
 
# Coding Part

import customtkinter as ctk

# Create the window
app = ctk.CTk()
app.title("Character Counter")
app.geometry("400x200")

# Function to update the character count
def update_count(event):
    text = entry.get()
    count = len(text)
    label.configure(text=f"Character Count: {count}")

# Entry box
entry = ctk.CTkEntry(app, width=250)
entry.pack(pady=20)

# Label
label = ctk.CTkLabel(app, text="Character Count: 0")
label.pack()

# Bind key release event
entry.bind("<KeyRelease>", update_count)

# Run the application
app.mainloop()
