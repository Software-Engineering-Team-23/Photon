import splash_screen # Splash screen
import first_screen # Player entry screen
import sql # Database backend wrapper
import udp # Networking
import tkinter as tk

def main():
    main_window = tk.Tk()
    splash_screen.splashScreen(main_window)
    first_screen.firstScreen(main_window)

if __name__ == "__main__":
    main()