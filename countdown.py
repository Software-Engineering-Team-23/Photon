import os
import time
import tkinter as tk
from PIL import Image, ImageTk
import action_display


# Folder containing the images
IMAGE_FOLDER = "countdown_images"
BACKGROUND_IMAGE = os.path.join(IMAGE_FOLDER, "background.tif")
ALERT_IMAGE = os.path.join(IMAGE_FOLDER, "alert-on.tif")
RED_LINE_IMAGE = os.path.join(IMAGE_FOLDER, "red.png")
GREEN_LINE_IMAGE = os.path.join(IMAGE_FOLDER, "green.png")
STATE1_IMAGE = os.path.join(IMAGE_FOLDER, "state1.png")
STATE2_IMAGE = os.path.join(IMAGE_FOLDER, "state2.png")

# Load number images
NUMBER_IMAGES = {str(i): os.path.join(IMAGE_FOLDER, f"{i}.tif") for i in range(31)}

class CountdownApp:
    def __init__(self, root, players=None):
        self.root = root
        self.players = players
        self.root.title("Photon Match Countdown")
        self.root.attributes("-fullscreen", True)  # Enable fullscreen mode
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Load and resize background image
        self.bg_image = Image.open(BACKGROUND_IMAGE).resize((screen_width, screen_height), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        self.canvas = tk.Canvas(root, width=screen_width, height=screen_height)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)
        
        # Placeholder for countdown numbers
        self.number_label = tk.Label(root, bg="black")
        self.number_label.place(relx=0.5, rely=0.582, anchor=tk.CENTER)
        
        # Placeholder for alert message
        self.alert_label = tk.Label(root, bg="black")
        self.alert_label.place(relx=0.503, rely=0.21, anchor=tk.CENTER)  # Position slightly lower
        
        # Placeholders for horizontal lines
        self.top_line_label = tk.Label(root, bg="black")
        self.top_line_label.place(relx=0.5, rely=0.02, anchor=tk.CENTER)
        
        self.bottom_line_label = tk.Label(root, bg="black")
        self.bottom_line_label.place(relx=0.5, rely=0.98, anchor=tk.CENTER)
        
        # Placeholders for vertical lines
        self.left_line_label = tk.Label(root, bg="black")
        self.left_line_label.place(relx=0.01, rely=0.5, anchor=tk.CENTER)
        
        self.right_line_label = tk.Label(root, bg="black")
        self.right_line_label.place(relx=0.99, rely=0.5, anchor=tk.CENTER)
        
        # Placeholders for side logos (on top of vertical lines)
        self.left_logo_label = tk.Label(root, bg="black")
        self.left_logo_label.place(relx=0.07, rely=0.5, anchor=tk.CENTER)
        
        self.right_logo_label = tk.Label(root, bg="black")
        self.right_logo_label.place(relx=0.93, rely=0.5, anchor=tk.CENTER)
        
        self.countdown(30)
    
    def countdown(self, count):

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        if count >= 0:
            # Load the corresponding number image
            number_image = Image.open(NUMBER_IMAGES[str(count)])
            number_image = number_image.resize((int(screen_width * 0.4219), int(screen_height * 0.25)), Image.LANCZOS)
            self.number_photo = ImageTk.PhotoImage(number_image)
            
            # Update label with the new image
            self.number_label.config(image=self.number_photo)
            
            # Toggle alert visibility
            if count % 2 == 0:  # Alert appears every other second
                alert_image = Image.open(ALERT_IMAGE)
                alert_image = alert_image.resize((int(screen_width * 0.8594), int(screen_height * 0.25)), Image.LANCZOS)
                self.alert_photo = ImageTk.PhotoImage(alert_image)
                self.alert_label.config(image=self.alert_photo)
            else:
                self.alert_label.config(image='')
            
            # Toggle horizontal lines
            line_image_path = RED_LINE_IMAGE if count % 2 == 0 else GREEN_LINE_IMAGE
            horizontal_line_image = Image.open(line_image_path).resize((int(screen_width * 0.9739) , int(screen_height * 0.0463)), Image.LANCZOS)
            horizontal_line_photo = ImageTk.PhotoImage(horizontal_line_image)
            self.top_line_label.config(image=horizontal_line_photo)
            self.bottom_line_label.config(image=horizontal_line_photo)
            self.top_line_label.image = horizontal_line_photo  # Keep reference
            self.bottom_line_label.image = horizontal_line_photo
            
            # Rotate and resize vertical lines
            vertical_line_image = Image.open(line_image_path).rotate(90, expand=True).resize((int(screen_width * 0.026), int(screen_height * 0.9537)), Image.LANCZOS)
            vertical_line_photo = ImageTk.PhotoImage(vertical_line_image)
            self.left_line_label.config(image=vertical_line_photo)
            self.right_line_label.config(image=vertical_line_photo)
            self.left_line_label.image = vertical_line_photo  # Keep reference
            self.right_line_label.image = vertical_line_photo
            
            # Toggle side logos
            logo_image_path = STATE1_IMAGE if count % 2 == 0 else STATE2_IMAGE
            logo_image = Image.open(logo_image_path).resize((int(screen_width * 0.0521), int(screen_height * 0.0926)), Image.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_image)
            self.left_logo_label.config(image=logo_photo)
            self.right_logo_label.config(image=logo_photo)
            self.left_logo_label.image = logo_photo  # Keep reference
            self.right_logo_label.image = logo_photo
            
            self.root.after(1000, self.countdown, count - 1)
        else:
            # Added to open action display after the countdown
            self.root.destroy()
            action_display.open_window(self.players)


def open_window(players):
    root = tk.Toplevel()
    CountdownApp(root, players)
    root.mainloop()
