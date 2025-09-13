import pygame

class Button:
    def __init__(self, ai_game, msg, width, height, x, y):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # 按照传入参数设置尺寸
        self.width, self.height = width, height
        self.button_color = (138, 29, 78)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # 创建按钮矩形，并设置到指定位置
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.topleft = (x, y)   # 用左上角定位

        # 准备按钮文本
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)