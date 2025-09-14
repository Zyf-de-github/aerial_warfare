import pygame
import random
import asyncio
import platform

# 音频管理类
class Sound:
    def __init__(self):
        self.sounds = {}  # 存储音效的字典
        pygame.mixer.init()  # 初始化 mixer



        # self.load_sound('boss_background','sound/boss_background.wav')
        # self.set_volume('boss_background',0.3)
        # self.load_sound('background','sound/background.wav')
        # self.set_volume('background',0.3)

        self.load_sound('boom','sound/boom.wav')
        self.load_sound('big_boom','sound/big_boom.flac')
        self.load_sound('upgrade','sound/upgrade.wav')
        self.set_volume('upgrade',0.2)
        self.load_sound('super_shot','sound/super_shot.wav')
        self.load_sound('dangerous','sound/dangerous.wav')
        self.set_volume('dangerous',0.2)

    def load_sound(self, name, file_path):
        try:
            sound = pygame.mixer.Sound(file_path)
            self.sounds[name] = sound
        except pygame.error as e:
            print(f"加载音效 {file_path} 失败: {e}")

    def play(self, name,times=0):
        if name in self.sounds:
            self.sounds[name].play(int(times))
        else:
            print(f"音效 {name} 未找到")


    def set_volume(self, name, volume):
        if name in self.sounds:
            self.sounds[name].set_volume(volume)
        else:
            print(f"音效 {name} 未找到")