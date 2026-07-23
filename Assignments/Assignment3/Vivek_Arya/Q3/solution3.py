'''
THEORY
1)We use min(frame_width / img_width, frame_height / img_height) instead of max() because it gives us the smaller scaling
  factor which ensures the maintaing of the aspect ratio beacuse it fits the rezized image into the frame with minimal 
  distortion. If we use max() instead it will expand one dimension of the image because there may be a possibility that
  the other dimension would need way lower scaling factor to be fit into the frame.

2)Python garbage collection is a memory mangaement system that removes the object(here images) that are not being used
  anymore. ImageTk. Thats why PhotoImage must be stored in a variable such as label.image because if no reference to the
  image exists, Python's Garbage Collector removes it from memory, causing the displayed image to disappear from the
  Tkinter window.

  '''
import customtkinter as ctk
from PIL import Image, ImageTk
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Resize")
        self.geometry("600x400")
        self.originalimage = Image.open("CubeCanvas_Speedcubing/Assignments/Assignment3/Vivek_Arya/Q3/spiderpunk.jpg")

        self.imagelabel = ctk.CTkLabel(self, text="")
        self.imagelabel.pack(fill="both", expand=True)
        self.updateimage()
        self.bind("<Configure>", self.updateimage)
        
    def updateimage(self, event=None):
        self.resize(
            self.originalimage,
            self.winfo_width(),
            self.winfo_height()
        )
    def resize(self, image, max_w, max_h):
        originalwidth, originalheight = image.size
        scale = min(
            max_w / originalwidth,
            max_h / originalheight
        )
        new_width = int(originalwidth * scale)
        new_height = int(originalheight * scale)

        resized = image.resize((new_width, new_height),Image.Resampling.LANCZOS)
        tk_image = ImageTk.PhotoImage(resized)
        self.imagelabel.configure(
            image=tk_image,
            text=""
        )
        self.imagelabel.image = tk_image
        print((new_width, new_height))
        return (new_width, new_height)
    
app = App()
app.mainloop()