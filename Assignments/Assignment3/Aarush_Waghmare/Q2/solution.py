# solution.py

# part a: theory
# 1. an event binding is basically registering an interrupt handler. you're telling the gui loop "when this specific signal/event happens on this widget, execute this function pointer."
# 2. 'command' is a high-level abstraction specifically for a widget's default action (like a button click). .bind() is lower-level; it lets you trap raw os events (like <KeyRelease>) and passes an event struct containing metadata (like which key was pressed) to the callback.
# 3. writing function() executes it immediately during initialization and assigns the return value to the button (usually a bug). writing just 'function' passes the memory address/function pointer so the event loop can execute it later when needed.
# 4. 'command' expects a bare function pointer that takes no arguments. if you need to pass variables to your callback, you use a lambda as a quick inline wrapper function to hold those parameters until it's executed.

import customtkinter as ctk

# init window
app = ctk.CTk()
app.geometry("400x200")
app.title("Q2 Event Binding")

# callback routine for our interrupt
# .bind passes an event object automatically, so we must include it in the signature even if we just read from the entry directly
def update_count(event):
    # read the current buffer from the entry widget
    current_text = entry.get()
    length = len(current_text)
    # update the label text
    count_label.configure(text=f"Character Count: {length}")

# allocate text entry box
entry = ctk.CTkEntry(app, width=250, placeholder_text="start typing...")
entry.pack(pady=20)

# allocate label for the counter
count_label = ctk.CTkLabel(app, text="Character Count: 0")
count_label.pack(pady=10)

# hook the interrupt: bind the specific KeyRelease event to our function pointer
entry.bind("<KeyRelease>", update_count)

# hand over control to the gui's main polling loop
app.mainloop()