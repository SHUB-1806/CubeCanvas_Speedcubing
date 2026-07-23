
# Theory 
# 1.We use min() so the image fits completely inside the frame without getting cropped. Using max() can make the image too large, causing parts of it to go outside the frame.
# 2.Python's Garbage Collection automatically removes objects that are no longer being used to free memory. We store a reference like label.image = tk_image so the image is not deleted; otherwise, it may disappear from the window.

# Coding part 

"""
THEORY (write at top as required):

1. Aspect ratio is preserved by scaling both width and height by the same factor.
2. The scaling factor is:
      min(max_w / original_width, max_h / original_height)
3. Lanczos resampling gives high-quality image resizing (best for downscaling).
"""

from PIL import Image, ImageTk
import tkinter as tk


def safe_resize(image_path, max_w, max_h):
    # 1. Open image
    img = Image.open(image_path)

    orig_w, orig_h = img.size

    # 2. Compute scaling factor (keep aspect ratio)
    scale = min(max_w / orig_w, max_h / orig_h)

    new_w = int(orig_w * scale)
    new_h = int(orig_h * scale)

    # 3. Resize using Lanczos
    resized_img = img.resize((new_w, new_h), Image.LANCZOS)

    # 4. Create Tkinter window
    root = tk.Tk()
    root.title("Safe Resize")

    # Convert image for Tkinter
    tk_img = ImageTk.PhotoImage(resized_img)

    # Display image
    label = tk.Label(root, image=tk_img)
    label.image = tk_img   # IMPORTANT (prevents blank window)
    label.pack()

    # Run GUI
    root.mainloop()

    # 5. Return new dimensions
    return (new_w, new_h)

if __name__ == "__main__":
    path = r"C:\Users\samskruthi\Downloads\Trump.jpeg"
    max_width = 400
    max_height = 400

    dims = safe_resize(path, max_width, max_height)
    print("New dimensions:", dims)
    
