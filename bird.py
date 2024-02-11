import pygame


# Bird Class to handle the bird sprite and its movement and animation
class Bird(pygame.sprite.Sprite):
    # Bird Class Constructor to initialize the bird sprite and its properties and settings 
    def __init__(self, x, y, settings):
        pygame.sprite.Sprite.__init__(self)
        self.game_started = False
        self.images = [
            pygame.image.load("assets/fb-bird1.png").convert_alpha(),
            pygame.image.load("assets/fb-bird2.png").convert_alpha(),
            pygame.image.load("assets/fb-bird3.png").convert_alpha(),
        ]
        self.current_image = 0
        self.counter = 0
        for i in range(len(self.images)):
            img = i
        self.image = self.images[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.velocity = 0
        self.clicked = False
        self.settings = settings

    # Bird Movement and Animation Method to handle the bird's movement and animation
    def update(self):
        # Check if the game has started and the bird is flying
        if self.settings.flying == True:
            # Add gravity when the user click the mouse
            self.velocity += 0.5
            if self.velocity > 8:
                self.velocity = 8
            if self.rect.top < 0:
                self.rect.y = 0
            if self.rect.bottom < 682:
                self.rect.y += int(self.velocity)
        # Check if the game is over and the bird is not flying
        if self.settings.game_over == False:
            # Check if the user clicked the mouse and handle the bird's movement
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.velocity = -10
                self.settings.wing_sound.play() 
            # Check if the user released the mouse button and reset the clicked variable
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            # Handle the animation
            self.counter += 1
            flap_cooldown = 5
            # Check if the counter is greater than the flap cooldown and update the bird's animation
            if self.counter > flap_cooldown:
                self.counter = 0
                self.current_image = (self.current_image + 1) % len(self.images)
                self.image = self.images[self.current_image]
            # Rotate the bird based on its velocity and update the bird's mask
            self.image = pygame.transform.rotate(
                self.images[self.current_image], self.velocity * -2
            )
        # Check if the game is over and the bird is not flying
        else:
            self.image = pygame.transform.rotate(self.images[self.current_image], -90)
