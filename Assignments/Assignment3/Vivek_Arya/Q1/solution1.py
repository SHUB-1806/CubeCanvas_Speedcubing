'''
THEORY
1)The purpose of weight parameter is to distribute the space in different rows and column whenever the window is resized. 
  A larger weight means that row will expand much greater than the row with low weight. If they have same weight then
  they will expand equally.
2)The argument Sticky="nsew" helps expand the widget to fill the entire grid. Here n,s,e,w means or represent north, south
  east and west.
3)The concept of stacking frames is placing mutiple frames in the same position but one on top of another such that the
  top one is visible and is the only visible one. The tkraise() method brings the selected frame to the front or top ,
  making it visible and other frames remains hidden behind it.

'''

import customtkinter as ctk
class App(ctk.CTk):
   def __init__(self):
      super().__init__()
      self.title("Grid Geometry")
      self.geometry("400x400")
       
      self.grid_rowconfigure(0, weight =1)
      self.grid_rowconfigure(1, weight =1)

      self.grid_columnconfigure(0, weight =1)
      self.grid_columnconfigure(1, weight =1)

      self.frame1 = ctk.CTkFrame(self,fg_color = "green")
      self.frame2 = ctk.CTkFrame(self,fg_color = "red")
      self.frame3 = ctk.CTkFrame(self,fg_color = "blue")
      self.frame4 = ctk.CTkFrame(self,fg_color = "yellow")
      
      self.frame1.grid(row=0,column=0,sticky="nsew")
      self.frame2.grid(row=0,column=1,sticky="nsew")
      self.frame3.grid(row=1,column=0,sticky="nsew")
      self.frame4.grid(row=1,column=1,sticky="nsew")
   
   
app =App()
app.mainloop()
