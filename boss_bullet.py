import pygame
from pygame.sprite import Sprite


class Boss_Bullet(Sprite):
    def __init__(self, ai_game, x_offset, y_offset, x_speed=0):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 加载子弹图片
        self.image = pygame.image.load('images/boss_bullet.png').convert_alpha()  # 确保bullet.png在项目目录
        scale = 0.05  # 缩小到 50%，你可以改成 0.25, 0.75, 2.0 等
        w, h = self.image.get_size()
        new_size = (int(w * scale), int(h * scale))
        self.image = pygame.transform.smoothscale(self.image, new_size)
        self.rect = self.image.get_rect()

        self.rect.midtop = ai_game.boss.rect.midtop
        self.rect.x += x_offset+20  # 应用x偏移
        self.rect.y += y_offset  # 应用y偏移

        # 存储浮点数位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.x_speed = x_speed

    def update(self):
        # 更新子弹位置
        self.y += self.settings.boss_bullet_speed
        self.x += self.x_speed
        self.rect.y = int(self.y)
        self.rect.x = int(self.x)

    def draw_bullet(self):
        # 绘制子弹图片
        self.screen.blit(self.image, self.rect)