import pygame
import os

class MusicPlayer:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.muted = False

    def play_music(self, file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.set_volume(100)  # 设置音量
        pygame.mixer.music.play(loops=-1)  # 循环播放

    def toggle_mute(self):
        if not self.muted:
            pygame.mixer.music.set_volume(0)  # 设置音量为0，实现静音
            self.muted = True
        else:
            pygame.mixer.music.set_volume(100)  # 恢复音量
            self.muted = False
        return self.muted