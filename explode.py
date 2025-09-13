import pygame
import random
from pygame.sprite import Sprite


class Explosion(Sprite):
    def __init__(self, center, ai_game, scale=1):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.scale = scale  # 缩放比例，默认1

        # 生成爆炸动画帧
        self.frames = self.generate_explosion_frames()

        # 设置当前帧
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = center

        # 动画计时器
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 60  # 每帧显示60毫秒

        # 爆炸粒子效果
        self.particles = self.create_particles(center)

    def generate_explosion_frames(self):
        """程序生成爆炸动画帧"""
        frames = []
        # 定义爆炸的大小和颜色变化序列
        base_sizes = [15, 30, 45, 60, 75, 90, 75, 60, 45, 30, 15]  # 基础大小
        sizes = [size * self.scale for size in base_sizes]  # 应用缩放
        colors = [
            (255, 255, 200),  # 亮黄色
            (255, 220, 100),  # 橙黄色
            (255, 180, 50),  # 橙色
            (255, 120, 0),  # 红橙色
            (255, 80, 0),  # 红色
            (255, 40, 0),  # 深红色
            (200, 20, 0),  # 暗红色
            (150, 10, 0),  # 更暗的红色
            (100, 5, 0),  # 几乎黑色
            (50, 0, 0),  # 黑色
            (0, 0, 0)  # 完全透明（消失）
        ]

        for i, (size, color) in enumerate(zip(sizes, colors)):
            # 创建透明表面，尺寸随缩放调整
            surface = pygame.Surface((size * 2 + 20 * self.scale, size * 2 + 20 * self.scale), pygame.SRCALPHA)

            # 绘制主爆炸圆形
            pygame.draw.circle(surface, (*color, 220), (size + 10 * self.scale, size + 10 * self.scale), size)

            # 添加光晕效果
            if i < 6:  # 前半段动画有光晕
                glow_size = size + 10 * self.scale
                for alpha in range(100, 30, -20):
                    pygame.draw.circle(surface, (255, 200, 100, alpha),
                                       (size + 10 * self.scale, size + 10 * self.scale), glow_size, 2)
                    glow_size -= 3 * self.scale

            # 添加随机火花效果
            if i < 8:  # 前8帧有火花
                for _ in range(int(size // 3)):
                    angle = random.uniform(0, 6.28)
                    distance = random.randint(int(size // 2), int(size))
                    x = size + 10 * self.scale + distance * pygame.math.Vector2(1, 0).rotate(angle * 57.3).x
                    y = size + 10 * self.scale + distance * pygame.math.Vector2(1, 0).rotate(angle * 57.3).y
                    spark_size = random.randint(2, 6) * self.scale
                    spark_color = (255, 255, 200, random.randint(150, 220))
                    pygame.draw.circle(surface, spark_color, (int(x), int(y)), int(spark_size))

            frames.append(surface)

        return frames

    def create_particles(self, center):
        """创建爆炸粒子效果"""
        particles = []
        for _ in range(20):
            angle = random.uniform(0, 6.28)
            speed = random.uniform(2, 8) * self.scale  # 速度随缩放调整
            size = random.randint(2, 6) * self.scale  # 粒子大小随缩放调整
            lifetime = random.randint(20, 40)
            color = random.choice([
                (255, 255, 200), (255, 200, 100),
                (255, 150, 50), (255, 100, 0)
            ])

            particles.append({
                'pos': [center[0], center[1]],
                'vel': [speed * pygame.math.Vector2(1, 0).rotate(angle * 57.3).x,
                        speed * pygame.math.Vector2(1, 0).rotate(angle * 57.3).y],
                'size': size,
                'color': color,
                'lifetime': lifetime,
                'age': 0
            })
        return particles

    def update(self):
        """更新爆炸动画和粒子"""
        now = pygame.time.get_ticks()

        # 更新主爆炸动画
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame_index += 1

            if self.frame_index >= len(self.frames):
                self.kill()  # 动画结束
            else:
                center = self.rect.center
                self.image = self.frames[self.frame_index]
                self.rect = self.image.get_rect()
                self.rect.center = center

        # 更新粒子效果
        for particle in self.particles:
            particle['pos'][0] += particle['vel'][0]
            particle['pos'][1] += particle['vel'][1]
            particle['age'] += 1
            particle['vel'][0] *= 0.95  # 减速
            particle['vel'][1] *= 0.95

        # 移除死亡的粒子
        self.particles = [p for p in self.particles if p['age'] < p['lifetime']]

    def draw(self, screen):
        """绘制爆炸和粒子"""
        # 绘制主爆炸
        if self.frame_index < len(self.frames):
            screen.blit(self.image, self.rect)

        # 绘制粒子
        for particle in self.particles:
            alpha = 255 * (1 - particle['age'] / particle['lifetime'])
            color = (*particle['color'], int(alpha))
            pos = (int(particle['pos'][0]), int(particle['pos'][1]))
            pygame.draw.circle(screen, color, pos, int(particle['size']))