import tkinter as tk
from tkinter import filedialog
import pygame
import random

pygame.mixer.init()

def play_music(filename, start_at=0.0):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(start=start_at)

def random_music(start_at=0.0):
    track_number = random.randint(1, 8)
    filename = f"audio_tracks/Track{track_number:02}.mp3"
    play_music(filename, start_at=start_at)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Music Sample")

    random_music()

    root.mainloop()
