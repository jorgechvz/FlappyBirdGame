import pygame


class Pipe(pygame.sprite.Sprite):
    # Pipe Class Constructor to initialize the pipe sprite and its properties and settings 
    def __init__(self, x, y, position, settings):
        # Call the parent class (Sprite) constructor to initialize the pipe sprite 
        pygame.sprite.Sprite.__init__(self)
        self.passed_pipe = False
        self.position = position
        self.image = pygame.image.load("assets/fb-pipe.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 600))
        self.rect = self.image.get_rect()
        self.settings = settings
        # Set the position of the pipe based on the position parameter 
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - self.settings.pip_gap]
        # Set the position of the pipe based on the position parameter
        if position == -1:
            self.rect.topleft = [x, y + self.settings.pip_gap / 2]

    # Pipe Movement Method to handle the pipe's movement and animation 
    def update(self):
        self.rect.x -= 4
        if self.rect.right < 0:
            self.kill()
