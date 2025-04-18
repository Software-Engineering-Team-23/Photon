import tkinter as tk
from PIL import ImageTk, Image
import first_screen

class splashScreen:
    def __init__(self, win):
        #Avoid to manually move window
        win.overrideredirect(True)

        #Setting default win/position
        width = win.winfo_screenwidth()
        height = win.winfo_screenheight()
        win.geometry('%dx%d+%d+%d' % (width*0.8, height*0.8, width*0.1, height*0.1))

        #Open image and make a copy for resizing
        self.img = Image.open('logo.jpg')
        self.img_copy = self.img.copy()
        self.background_image = ImageTk.PhotoImage(self.img_copy)

        self.background = tk.Label(win, image=self.background_image)
        self.background.pack(fill=tk.BOTH, expand=tk.YES)

        self.background.bind('<Configure>', self.resize_background)

        win.after(3000, lambda: (win.destroy(), first_screen.open_window()))


    #function allows to resize the image file to window size
    def resize_background(self, event):
        nwidth = event.width
        nheight = event.height

        try:
            resample_filter = Image.Resampling.LANCZOS
        except AttributeError:
            resample_filter = Image.ANTIALIAS

        new_image = self.img_copy.resize((nwidth, nheight), resample_filter)
        self.background_image = ImageTk.PhotoImage(new_image)
        self.background.configure(image=self.background_image)

def open_window():
    win = tk.Tk()
    splashScreen(win)
    win.mainloop()
