import tkinter as tk
from tkinter import filedialog
import pygame
import random

pygame.mixer.init()

def play_music(filename):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

def random_music():
    track_number = random.randint(1,8)
    play_music(f"audio_tracks/Track0{track_number}.mp3")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Music Sample")

    play_music("audio_tracks/Track01.mp3")

    root.mainloop()