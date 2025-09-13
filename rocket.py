import pygame
import random
from pygame.sprite import Sprite

class Rocket(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load('images/rocket.png').convert_alpha()

        scale = 0.07  # 缩小到 50%，你可以改成 0.25, 0.75, 2.0 等
        w, h = self.image.get_size()
        new_size = (int(w * scale), int(h * scale))
        self.image = pygame.transform.smoothscale(self.image, new_size)
        self.rect = self.image.get_rect()


        self.rect.x=random.randint(1, self.settings.screen_width)
        self.y = float(0)

    def update(self):  # 重写函数
        self.y += self.settings.rocket_speed
        self.rect.y = int(self.y)

    def draw_rocket(self):
        self.screen.blit(self.image, self.rect)

