import sys
import pygame
from pygame.examples.midi import fill_region

import boss
from setting import Settings
from ship import Ship
from bullet import Bullet
from enemy import Enemy
from explode import Explosion
from button import Button
from upgrade import Upgrade
from rocket import Rocket
from boss import Boss
from boss_bullet import Boss_Bullet
import random

class Fight:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0,0),pygame.RESIZABLE)
        self.settings.screen_width=self.screen.get_width()
        self.settings.screen_height=self.screen.get_height()
        self.bg_color = self.settings.bg_color
        pygame.display.set_caption('Fight')
        self.ship = Ship(self)
        self.boss = None
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.upgrades = pygame.sprite.Group()
        self.rockets = pygame.sprite.Group()
        self.boss_bullets = pygame.sprite.Group()

        self.enemy_probability=self.settings.enemy_probability
        self.remain_enemies=self.settings.remain_enemies
        self.grade=self.settings.grade
        self.game_state=0   #0:开始界面 1:说明界面 2:游戏开始 3:boss战
        self.life_times=self.settings.life_times
        self.play_button = Button(self, 'Play',200,70,self.settings.screen_width/2-100, self.settings.screen_height/2-125)
        self.instruction_button = Button(self, 'instruction_button',400,70,self.settings.screen_width/2-200, self.settings.screen_height/2+25)
        self.back_button = Button(self, 'Back',200,70,self.settings.screen_width/2-100, self.settings.screen_height-125)
        self.live_button = Button(self, 'Lives:'+str(self.life_times),200,50,0,0)

        self.instructions = [
            "Game Instructions",
            "Controls:",
            "  - Arrow  keys:  Move  the  spaceship",
            "  - Auto-fire:  Shoots  bullets  at  intervals",
            "Objective:",
            "  - Collect  upgrades  to  enhance  firepower(up  to  level  6)",
            "Tips:",
            "  - Hitting  enemies  may  drop  upgrade  items",
            "  - Colliding  with  enemies  reduces  life  and  lowers  two  levels",
            "  - Game  ends  when  lives  reach  0"
        ]

        self.AUTO_FIRE_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.AUTO_FIRE_EVENT, int( self.settings.bullets_speed * 1000))  # 每 500 毫秒触发一次事件


        self.SUPER_SHOOTING_EVENT_STOP = pygame.USEREVENT + 2
        pygame.time.set_timer(self.SUPER_SHOOTING_EVENT_STOP, 0)

        self.BOSS_FIRE_EVENT = pygame.USEREVENT + 3
        pygame.time.set_timer(self.BOSS_FIRE_EVENT, 0)  # 每 500 毫秒触发一次事件

    def run_game(self):
        while True:
                self.check_events()
                if self.game_state>=2:
                    self.ship.update()
                    self.bullets.update()
                    self.enemies.update()
                    self.rockets.update()
                    self.enemies_coming()
                    self.rockets_coming()
                if self.game_state==3:
                    self.hit_boss()
                    if self.boss is not None:
                        self.boss_bullets.update()
                        self.boss.update()
                        self.boss_collisions()
                self.update_screen()
                self.clean_up()
                self.check_collisions()
                self.check_upgrades()
                self.explosions.update()
                self.hit_rocket()
                self.losing_game()


    def losing_game(self):
        if pygame.sprite.spritecollideany(self.ship, self.enemies):
            self.life_times -= 1
            self.grade -= 2
            if self.grade < 1:
                self.grade = 1
            # print('Game Over')
            for enemy in self.enemies:
                # 在敌人位置创建爆炸
                explosion = Explosion(enemy.rect.center, self)
                self.explosions.add(explosion)
            explosion = Explosion(self.ship.rect.center, self)
            self.explosions.add(explosion)
            self.enemies.empty()
            self.bullets.empty()
            self.upgrades.empty()
            self.rockets.empty()
            self.live_button = Button(self, 'Lives:' + str(self.life_times), 200, 50, 0, 0)
            self.ship.__init__(self)
            if self.life_times < 0:
                self.game_state=0
                pygame.mouse.set_visible(True)

    def hit_rocket(self):
        if pygame.sprite.spritecollideany(self.ship, self.rockets):
            self.life_times -= 1
            self.grade -= 2
            if self.grade < 1:
                self.grade = 1
            for rocket in self.rockets:
                # 在敌人位置创建爆炸
                explosion = Explosion(rocket.rect.center, self)
                self.explosions.add(explosion)
            explosion = Explosion(self.ship.rect.center, self)
            self.explosions.add(explosion)
            self.enemies.empty()
            self.bullets.empty()
            self.upgrades.empty()
            self.rockets.empty()
            self.live_button = Button(self, 'Lives:' + str(self.life_times), 200, 50, 0, 0)
            self.ship.__init__(self)
            if self.life_times < 0:
                self.game_state=0
                pygame.mouse.set_visible(True)

    def hit_boss(self):
        if self.boss is not None:
            boss_collisions = pygame.sprite.spritecollide(self.boss, self.bullets, True)  # 获取碰撞的子弹
            for bullet in boss_collisions:  # 只处理实际碰撞的子弹
                self.boss.boss_blood -= 1
                explosion = Explosion(bullet.rect.center, self,0.3)  # 子弹命中位置爆炸
                self.explosions.add(explosion)
            if self.boss.boss_blood <= 0:
                explosion = Explosion(self.boss.rect.center, self,3)  # Boss死亡时大爆炸
                self.explosions.add(explosion)
                self.game_state=2
                self.boss=None
                pygame.time.set_timer(self.BOSS_FIRE_EVENT, 0)  # 每 500 毫秒触发一次事件

    def boss_collisions(self):
        if self.game_state == 3 and self.boss:
            # 飞船与Boss碰撞
            boss_bullet_collisions = pygame.sprite.spritecollide(self.ship, self.boss_bullets, True)
            if pygame.sprite.collide_rect(self.ship, self.boss) or boss_bullet_collisions:
                self.life_times -= 1
                self.grade = max(1, self.grade - 2)
                explosion = Explosion(self.ship.rect.center, self, scale=1)
                self.explosions.add(explosion)
                self.enemies.empty()
                self.bullets.empty()
                self.upgrades.empty()
                self.rockets.empty()
                self.live_button = Button(self, 'Lives:' + str(self.life_times), 200, 50, 0, 0)
                self.ship.__init__(self)
                if self.life_times < 0:
                    self.game_state = 0
                    pygame.mouse.set_visible(True)


    def clean_up(self):
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            for enemy in self.enemies.copy():
                if enemy.rect.bottom >= self.settings.screen_height:
                    self.enemies.remove(enemy)
            for rocket in self.rockets.copy():
                if rocket.rect.bottom >= self.settings.screen_height:
                    self.rockets.remove(rocket)
            # print('子弹数量:'+str(len(self.bullets))+' 敌机数量:'+str(len(self.enemies)))

    def check_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        # 为每个被击中的敌人创建爆炸效果
        for bullet, hit_enemies in collisions.items():
            for enemy in hit_enemies:
                explosion = Explosion(enemy.rect.center, self)
                self.explosions.add(explosion)
                if random.randint(1, 30) <= self.settings.upgrade_probability - self.grade:
                    self.upgrade_ship(enemy.rect.center)


    def check_upgrades(self):
        collided_upgrades = pygame.sprite.spritecollide(self.ship, self.upgrades, True)
        # 为每个被击中的敌人创建爆炸效果
        for upgrades in collided_upgrades:
            if self.grade<6:
                self.grade += 1
            else:
                pygame.time.set_timer(self.AUTO_FIRE_EVENT, int(self.settings.super_bullets_speed*1000))
                pygame.time.set_timer(self.SUPER_SHOOTING_EVENT_STOP, int(self.settings.super_fire_timer * 1000))
                self.bg_color = (255, 190, 190)

    def check_events(self):
        for event in pygame.event.get():
            # 退出游戏
            if event.type == pygame.QUIT:
                sys.exit()

            # 鼠标点击开始按钮
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.game_state==0:
                    if self.play_button.rect.collidepoint(mouse_pos):
                        self.life_times=self.settings.life_times
                        self.live_button = Button(self, 'Lives:' + str(self.life_times), 200, 50, 0, 0)
                        pygame.mouse.set_visible(False)
                        self.game_state = 2
                    if self.instruction_button.rect.collidepoint(mouse_pos):
                        self.game_state = 1
                if self.game_state==1:
                    if self.back_button.rect.collidepoint(mouse_pos):
                        self.game_state = 0

            # 按键松开 0 退出
            elif event.type == pygame.KEYUP and event.key == pygame.K_0:
                sys.exit()

            # 游戏进行中才响应键盘事件
            if self.game_state>=2:
                # 按键按下
                if event.type == self.AUTO_FIRE_EVENT:
                    self.fire_bullet()
                if event.type == self.SUPER_SHOOTING_EVENT_STOP:
                    pygame.time.set_timer(self.AUTO_FIRE_EVENT, int(self.settings.bullets_speed * 1000))
                    pygame.time.set_timer(self.SUPER_SHOOTING_EVENT_STOP, 0)
                    self.bg_color = self.settings.bg_color
                if self.game_state==3 and self.boss and event.type ==self.BOSS_FIRE_EVENT:
                    self.boss_fire_bullet()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.ship.moving_left = True
                    elif event.key == pygame.K_RIGHT:
                        self.ship.moving_right = True
                    elif event.key == pygame.K_UP:
                        self.ship.moving_up = True
                    elif event.key == pygame.K_DOWN:
                        self.ship.moving_down = True

                # 按键抬起
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.ship.moving_left = False
                    elif event.key == pygame.K_RIGHT:
                        self.ship.moving_right = False
                    elif event.key == pygame.K_UP:
                        self.ship.moving_up = False
                    elif event.key == pygame.K_DOWN:
                        self.ship.moving_down = False

    def enemies_coming(self):
        temp = random.randint(1, 30000)
        if len(self.enemies)<self.settings.enemy_max_num and temp <= self.enemy_probability:
            new_enemy = Enemy(self)
            self.enemies.add(new_enemy)
            if self.game_state!=3:
                self.remain_enemies-=1
            if self.remain_enemies==0:
                self.game_state = 3
                self.boss = Boss(self)
                self.enemy_probability=self.settings.enemy_probability/2
                self.remain_enemies=self.settings.remain_enemies
                pygame.time.set_timer(self.BOSS_FIRE_EVENT, int(self.settings.boss_fire_speed*1000))  # 每 500 毫秒触发一次事件


    def rockets_coming(self):
        temp = random.randint(1, 30000)
        if len(self.rockets)<self.settings.rocket_max_num and temp <= self.settings.rocket_probability:
            new_rocket = Rocket(self)
            self.rockets.add(new_rocket)

    def upgrade_ship(self,center):
        new_upgrade = Upgrade(self,center)
        self.upgrades.add(new_upgrade)

    def boss_fire_bullet(self):
        new_boss_bullet = Boss_Bullet(self, 0, 0)
        self.boss_bullets.add(new_boss_bullet)
        new_boss_bullet = Boss_Bullet(self, -20, -10,-0.3)
        self.boss_bullets.add(new_boss_bullet)
        new_boss_bullet = Boss_Bullet(self, 20, -10,0.3)
        self.boss_bullets.add(new_boss_bullet)

    def fire_bullet(self):
        new_bullet = Bullet(self,0,0)
        self.bullets.add(new_bullet)
        if self.grade >= 2:
            new_bullet_left_0 = Bullet(self, -20,20,-0.1)  # 向左偏移20像素
            self.bullets.add(new_bullet_left_0)
            new_bullet_right_0 = Bullet(self, 20,20,0.1)  # 向右偏移20像素
            self.bullets.add(new_bullet_right_0)
        if self.grade >= 3:
            new_bullet_left_1 = Bullet(self, -25,25,-0.2)  # 向左偏移20像素
            self.bullets.add(new_bullet_left_1)
            new_bullet_right_1 = Bullet(self, 25,25,0.2)  # 向右偏移20像素
            self.bullets.add(new_bullet_right_1)
        if self.grade >= 4:
            new_bullet_left_2 = Bullet(self, -30, 30, -0.3)  # 向左偏移20像素
            self.bullets.add(new_bullet_left_2)
            new_bullet_right_2 = Bullet(self, 30, 30, 0.3)  # 向右偏移20像素
            self.bullets.add(new_bullet_right_2)
        if self.grade >= 5:
            new_bullet_left = Bullet(self, -10,10)  # 向左偏移20像素
            self.bullets.add(new_bullet_left)
            new_bullet_right = Bullet(self, 10,10)  # 向右偏移20像素
            self.bullets.add(new_bullet_right)
        if self.grade >= 6:
            new_bullet_back = Bullet(self, 0,40)  # 向左偏移20像素
            self.bullets.add(new_bullet_back)
            new_bullet_left_back = Bullet(self, -10,40)  # 向左偏移20像素
            self.bullets.add(new_bullet_left_back)
            new_bullet_right_back = Bullet(self, 10,40)  # 向右偏移20像素
            self.bullets.add(new_bullet_right_back)


    def update_screen(self):
        self.screen.fill(self.bg_color)
        self.live_button.draw_button()
        if self.game_state== 0:
            self.play_button.draw_button()
            self.instruction_button.draw_button()
        elif self.game_state == 1:
            line_height = 40  # 每行间隔 40 像素
            total_text_height = len(self.instructions) * line_height  # 总文本高度
            start_y = (self.settings.screen_height - total_text_height) // 2  # 垂直居中的起始 y 坐标

            for i, line in enumerate(self.instructions):
                text_surface = pygame.font.Font(None, 28).render(line, True, (0, 0, 0))  # 黑色文本
                text_rect = text_surface.get_rect()
                text_rect.centerx = self.settings.screen_width // 2  # 水平居中
                text_rect.y = start_y + i * line_height  # 每行间隔 40 像素
                self.screen.blit(text_surface, text_rect)
            self.back_button.draw_button()
        elif self.game_state >= 2 :
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            for enemy in self.enemies.sprites():
                enemy.draw_enemy()
            for rocket in self.rockets.sprites():
                rocket.draw_rocket()
            for explosion in self.explosions.sprites():
                explosion.draw(self.screen)  # 使用自定义的draw方法
            for upgrade in self.upgrades.sprites():
                if upgrade.upgrade_hit_times > self.settings.upgrade_hit_times:
                    self.upgrades.remove(upgrade)
                upgrade.update()
                upgrade.blitme()
            if self.game_state == 3 and self.boss is not None:
                for boss_bullet in self.boss_bullets.sprites():
                    boss_bullet.draw_bullet()
                self.boss.update()
                self.boss.draw_boss()

        pygame.display.flip()



if __name__ == '__main__':
    fight = Fight()
    fight.run_game()