import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, ai_game, x_offset, y_offset, x_speed=0):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 加载子弹图片
        self.image = pygame.image.load('images/bullet.png')  # 确保bullet.png在项目目录
        self.rect = self.image.get_rect()  # 获取图片的矩形用于定位和碰撞
        self.image = pygame.transform.scale(self.image, (self.settings.bullet_width, self.settings.bullet_height))  # 比如 (10, 20)
        # 设置子弹初始位置（基于飞船位置）
        self.rect.midtop = ai_game.ship.rect.midtop
        self.rect.x += x_offset+20  # 应用x偏移
        self.rect.y += y_offset  # 应用y偏移

        # 存储浮点数位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.x_speed = x_speed

    def update(self):
        # 更新子弹位置
        self.y -= self.settings.bullet_speed
        self.x += self.x_speed
        self.rect.y = int(self.y)
        self.rect.x = int(self.x)

    def draw_bullet(self):
        # 绘制子弹图片
        self.screen.blit(self.image, self.rect)