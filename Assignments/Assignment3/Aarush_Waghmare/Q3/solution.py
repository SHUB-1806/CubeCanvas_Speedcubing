# solution.py

# part a: theory
# 1. using max() scales the image based on the axis with the most headroom, which guarantees the other axis will overflow your frame bounds (classic buffer overflow logic). using min() forces the scaling to respect the tightest constraint, ensuring the whole image array fits safely inside the viewable memory/bounds.
# 2. python uses a garbage collector driven by reference counting (like automatic free()). when a python function ends, local variables are destroyed. if the tk image only existed in that local scope, python drops its ref count to 0 and frees the memory. however, the underlying c/tcl engine is still trying to render it, leaving tk with a dangling pointer that renders as a blank square. binding it to the widget (label.image = ptr) forces python to keep a reference alive.

import customtkinter as ctk
from PIL import Image, ImageTk
import os

# part b: coding
def safe_resize(image_path, max_w, max_h):
    # read file into memory buffer
    img = Image.open(image_path)
    img_w, img_h = img.size
    
    # calculate float scale factors for both axes
    scale_w = max_w / img_w
    scale_h = max_h / img_h
    
    # take the stricter bounding constraint
    scale = min(scale_w, scale_h)
    
    # calculate new geometry, casting to int for discrete pixel boundaries
    new_w = int(img_w * scale)
    new_h = int(img_h * scale)
    
    # apply lanczos filter for high quality downsampling
    resized_img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # return the manipulated image object and the geometry tuple
    return resized_img, (new_w, new_h)


# test code to satisfy submission requirements
if __name__ == "__main__":
    # init main window
    app = ctk.CTk()
    app.title("Q3 Image Resizing")
    
    # define our max bounds constraints
    win_w, win_h = 600, 400
    app.geometry(f"{win_w}x{win_h}")
    
    # setup a dummy image file just so the test runs immediately without needing external files
    dummy_path = "test_target.jpg"
    if not os.path.exists(dummy_path):
        # allocate a large pink rectangle to act as our source file
        dummy = Image.new('RGB', (1920, 1080), color="#FF00C8")
        dummy.save(dummy_path)
    
    # 1. call our routine, passing the window dimensions as constraints
    # subtracting a little padding so it doesn't touch the absolute edges
    processed_image, dimensions = safe_resize(dummy_path, win_w - 40, win_h - 40)
    
    print(f"successfully calculated new bounds: {dimensions[0]}x{dimensions[1]}")
    
    # 2. cast the PIL image to a Tkinter compatible format
    tk_img = ImageTk.PhotoImage(processed_image)
    
    # 3. allocate label and render
    label = ctk.CTkLabel(app, text="", image=tk_img)
    
    # CRITICAL: storing the pointer so the garbage collector doesn't free our image buffer
    label.image = tk_img 
    
    label.pack(expand=True)
    
    # hand over to event loop
    app.mainloop()