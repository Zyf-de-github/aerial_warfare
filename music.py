import pygame
import time

import pygame
import time

class Music:
    def __init__(self, game):
        self.game = game  # 引用游戏对象以访问 game_state
        self.current_music = None  # 跟踪当前播放的音乐
        self.fade_out_start_time = None  # 淡出开始时间
        self.fade_out_duration = 1.0  # 淡出持续 1 秒
        self.fade_in_start_time = None  # 淡入开始时间
        self.fade_in_duration = 1.0  # 淡入持续 1 秒
        self.target_music = None  # 目标音乐
        pygame.mixer.init()  # 初始化 mixer
        self.music_files = {
            'background': 'sound/background.wav',
            'boss_background': 'sound/boss_background.wav'
        }
        self.volume = 0.2  # 默认音量
        pygame.mixer.music.set_volume(self.volume)

    def update(self):
        """根据 game_state 更新背景音乐"""
        # 确定目标音乐
        target_music = 'boss_background' if self.game.game_state == 3 else 'background'

        # 如果目标音乐与当前音乐相同，且不在淡入淡出过程中，直接返回
        if self.current_music == target_music and not self.fade_out_start_time and not self.fade_in_start_time:
            return

        current_time = time.time()

        # 处理淡出
        if self.fade_out_start_time:
            elapsed = current_time - self.fade_out_start_time
            if elapsed >= self.fade_out_duration:
                pygame.mixer.music.stop()  # 淡出完成后停止音乐
                self.fade_out_start_time = None
                # 加载并开始播放新音乐
                if self.target_music:
                    try:
                        pygame.mixer.music.load(self.music_files[self.target_music])
                        pygame.mixer.music.set_volume(0.0)  # 初始音量为 0
                        pygame.mixer.music.play(-1)  # 循环播放
                        self.fade_in_start_time = current_time
                        self.current_music = self.target_music
                        self.target_music = None
                    except pygame.error as e:
                        print(f"加载背景音乐 {self.target_music} 失败: {e}")
                        self.current_music = None
                        self.target_music = None
            else:
                # 计算淡出音量（从 volume 到 0）
                volume = self.volume * (1 - elapsed / self.fade_out_duration)
                pygame.mixer.music.set_volume(max(0.0, volume))
            return

        # 处理淡入
        if self.fade_in_start_time:
            elapsed = current_time - self.fade_in_start_time
            if elapsed >= self.fade_in_duration:
                pygame.mixer.music.set_volume(self.volume)  # 恢复目标音量
                self.fade_in_start_time = None
            else:
                # 计算淡入音量（从 0 到 volume）
                volume = self.volume * (elapsed / self.fade_in_duration)
                pygame.mixer.music.set_volume(min(self.volume, volume))
            return

        # 没有淡入淡出时，检查是否需要切换音乐
        if self.current_music != target_music:
            self.target_music = target_music
            if self.current_music:
                self.fade_out_start_time = current_time  # 开始淡出
                pygame.mixer.music.set_volume(self.volume)  # 确保淡出从全音量开始
            else:
                # 没有当前音乐，直接加载并播放
                try:
                    pygame.mixer.music.load(self.music_files[target_music])
                    pygame.mixer.music.set_volume(0.0)  # 初始音量为 0
                    pygame.mixer.music.play(-1)  # 循环播放
                    self.fade_in_start_time = current_time
                    self.current_music = target_music
                    self.target_music = None
                except pygame.error as e:
                    print(f"加载背景音乐 {target_music} 失败: {e}")
                    self.current_music = None
                    self.target_music = None

    def set_volume(self, volume):
        """设置背景音乐音量"""
        self.volume = volume
        if not self.fade_in_start_time and not self.fade_out_start_time:
            pygame.mixer.music.set_volume(volume)