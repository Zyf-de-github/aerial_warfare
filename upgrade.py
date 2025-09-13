import pygame
import random
from pygame.sprite import Sprite

class Upgrade(Sprite):
    def __init__(self,ai_game,center):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load('images/upgrade.png').convert_alpha()

        scale = 0.25  # 缩小到 50%，你可以改成 0.25, 0.75, 2.0 等
        w, h = self.image.get_size()
        new_size = (int(w * scale), int(h * scale))
        self.image = pygame.transform.smoothscale(self.image, new_size)
        self.rect = self.image.get_rect()

        self.rect.center = center
        self.upgrade_hit_times=0
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.moving_right_or_left = random.choice([1, -1])
        self.moving_up_or_down = random.choice([1, -1])

    def update(self):
        # 先移动
        self.x += self.settings.upgrade_speed * self.moving_right_or_left
        self.y += self.settings.upgrade_speed * self.moving_up_or_down

        # 左右边界检查
        if self.x + self.rect.width >= self.screen_rect.right:
            self.x = self.screen_rect.right - self.rect.width
            self.upgrade_hit_times += 1
            self.moving_right_or_left *= -1
        if self.x <= 0:
            self.x = 0
            self.moving_right_or_left *= -1
            self.upgrade_hit_times += 1


        # 上下边界检查
        if self.y + self.rect.height >= self.screen_rect.bottom:
            self.y = self.screen_rect.bottom - self.rect.height
            self.moving_up_or_down *= -1
            self.upgrade_hit_times += 1

        if self.y <= 0:
            self.y = 0
            self.moving_up_or_down *= -1
            self.upgrade_hit_times += 1


        # 更新 rect
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

