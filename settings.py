import pygame


class Settings:
    def __init__(self):
        # Game Window Dimensions and Clock Speed (Frames Per Second)
        self.WIDTH = 864
        self.HEIGHT = 936
        self.CLOCK = pygame.time.Clock()
        self.FPS = 60
        # Bird Settings
        self.game_over = False
        self.flying = False
        # Pipe Settings
        self.pip_gap = 150
        self.pip_distance = 300
        self.pipe_frequency = 1500
        self.last_pipe = pygame.time.get_ticks() - self.pipe_frequency
