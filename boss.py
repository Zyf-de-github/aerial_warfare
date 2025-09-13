import pygame
import random
from pygame.sprite import Sprite

class Boss(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.boss_blood = self.settings.boss_blood
        self.image = pygame.image.load('images/boss.png').convert_alpha()

        scale = 0.5  # 缩小到 50%，你可以改成 0.25, 0.75, 2.0 等
        w, h = self.image.get_size()
        new_size = (int(w * scale), int(h * scale))
        self.image = pygame.transform.smoothscale(self.image, new_size)
        self.rect = self.image.get_rect()

        self.y = float(0)
        self.x=self.settings.screen_width/2-self.rect.width/2
        self.rect.x = self.x
        self.state=1

    def update(self):  # 重写函数
        if self.y<150:
            self.y += self.settings.boss_speed
        else:
            if self.rect.x>=self.settings.screen_width-self.rect.width:
                self.state*=-1
            if self.rect.x<=self.rect.width:
                self.state*=-1
            self.x +=self.settings.boss_speed*self.state
        self.rect.y = int(self.y)
        self.rect.x = int(self.x)

    def draw_boss(self):
        self.screen.blit(self.image, self.rect)

