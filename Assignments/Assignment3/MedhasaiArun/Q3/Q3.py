# PART A
# 1. We use min() because we want to fit it inside the frame boundaries. If we use max(), there is a possibilty of the image overshooting
#  outside the frame boundaries. Example : IMAGE - 500X500 and FRAME- 400X200 --> This means fwid/imwid=0.8 and fh/imh=0.4 
#  So if we use min(), we get 0.4 and the image is scaled down to 40% of its size which fits inside the frame and nothing gets cut off. 
#  If we use max(), part of the image gets cut off.
# 2. Python's garbage collector is an automatic memory cleanup system. It scans our program for any data objects that don't have an 
#  active variable or a name and permanently deletes them from memory to free up space, assuming that they are unimportant. When you 
#  convert a Pillow image to a Tkinter-compatible image format inside any function, Tkinter uses the image data, but Python itself loses 
#  track of the local variable name once the function finishes running. Then the garbage collector deletes the data. To prevent this we must 
#  store the image using ImageTk.PhotoImage.

#PART B
from PIL import Image,ImageTk
import customtkinter as ctk

def safe_resize(image_path,max_w,max_h):
        img=Image.open(image_path)
        #print(img.size)
        img_w,img_h=img.size 
        
        scale=min(max_w/img_w,max_h/img_h)
        new_w=int(scale*img_w)
        new_h=int(scale*img_h)
        
        resized_img=img.resize((new_w,new_h),Image.Resampling.LANCZOS)
        #display(resized_img)
        
        window=ctk.CTk()
        window.title("Q3 IMAGE VIEWER")
       
        window.geometry(str(new_w)+"x"+str(new_h))
        tk_img = ImageTk.PhotoImage(resized_img)
        label = ctk.CTkLabel(window, image=tk_img, text="")
        label.pack(expand=True)
        
        label.image = tk_img 
        
        window.mainloop()
        return(new_w,new_h)

result_img = safe_resize(r"C:\Users\ARUN\Downloads\shiba.jpg", 500, 400)
print("Final Dimensions:",result_img)