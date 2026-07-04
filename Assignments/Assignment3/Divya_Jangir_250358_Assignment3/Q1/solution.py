# 1. The weight parameter decides how extra space is distributed among rows and columns when the window is resized.
# 2. It makes a widget stretch in all 4 directions so it fills its entire grid cell.
# 3. Stacking frames means placing multiple frames in the same location and displaying only one at a time. The tkraise() method brings the selected frame to the fromt.
import customtkinter as ctk

app = ctk.CTk()
app.title("Question 1")
app.geometry("400*400")


for i in range(2):
    app.grid_rowconfigure(i, weight=1)
    app.grid_columnconfigure(i, weight=1)

colors = ["red", "green", "blue", "yellow"]

index = 0
for row in range(2):
    for col in range(2):
        frame = ctk.CTkFrame(app, fg_color=colors[index])
        frame.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
        index += 1
app.mainloop()
