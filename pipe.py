import pygame


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position, settings):
        pygame.sprite.Sprite.__init__(self)
        self.passed_pipe = False
        self.position = position
        self.image = pygame.image.load("assets/fb-pipe.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 600))
        self.rect = self.image.get_rect()
        self.settings = settings
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - self.settings.pip_gap]
        if position == -1:
            self.rect.topleft = [x, y + self.settings.pip_gap / 2]

    def update(self):
        self.rect.x -= 4
        if self.rect.right < 0:
            self.kill()
