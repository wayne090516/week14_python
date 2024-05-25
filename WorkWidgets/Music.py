import pygame
import threading
import os

class Music:
    def __init__(self, file_path):
        pygame.mixer.init()
        self.is_loaded = threading.Event()
        self.file_path = file_path
        self.volume = 1
        
        try:
            pygame.mixer.music.load(self.file_path)
            self.is_loaded.set()
        except Exception as e:
            print(f"Error loading music file: {e}")
        
        self.is_playing = threading.Event()

    def set_volume(self, value):
        self.volume = value / 100.0
        pygame.mixer.music.set_volume(self.volume)

    def play(self):
        if not self.is_playing.is_set() and self.is_loaded.is_set():
            self.is_playing.set()
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1)
        
    def stop(self):
        if self.is_playing.is_set():
            self.is_playing.clear()
            pygame.mixer.music.stop()

