# Bare bones action display screen solely to connect to main program with F5
import tkinter as tk
from PIL import ImageTk, Image

class actionDisplay:
    def __init__(self, window):
        window.title("Action Display")
        window.geometry("800x700")
        window.configure(bg="black")

def open_window():
    window = tk.Tk()
    actionDisplay(window)
    window.mainloop()