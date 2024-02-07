import pygame
from settings import Settings
from pygame.locals import *
from bird import Bird
from pipe import Pipe
import random
from button import Button

# Flappy Bird Game Main File
pygame.init()

settings = Settings()

# Game Window
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Scroll Background
bg_scroll = 0
bg_speed = 4

# Set background image and scale it to fit the screen
bg_sky_image = pygame.image.load("assets/fb-background.png").convert()
bg_sky_image = pygame.transform.scale(bg_sky_image, (settings.WIDTH, settings.HEIGHT))
bg_ground_image = pygame.image.load("assets/fb-ground.png").convert()
button_img = pygame.image.load("assets/fb-restart.png").convert()

# Instantiate Bird Class
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy_bird = Bird(int(settings.WIDTH / 2), int(settings.HEIGHT / 2), settings)
bird_group.add(flappy_bird)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_game():
    pipe_group.empty()
    flappy_bird.rect.x = int(settings.WIDTH / 2)
    flappy_bird.rect.y = int(settings.HEIGHT / 2)


# Create a restart button
restart_button = Button(
    settings.WIDTH // 2 - 50, settings.HEIGHT // 2 - 100, button_img
)

run = True
while run:
    settings.CLOCK.tick(settings.FPS)

    # Draw background image
    screen.blit(bg_sky_image, (0, 0))

    # Draw and Update Bird
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    screen.blit(bg_ground_image, (bg_scroll, 682))

    if settings.game_over:
        if restart_button.draw(screen):
            settings.game_over = False
            reset_game()

    if (
        pygame.sprite.groupcollide(bird_group, pipe_group, False, False)
        or flappy_bird.rect.top < 0
    ):
        settings.game_over = True
        settings.flying = False

    if flappy_bird.rect.bottom > 682:
        settings.game_over = True
        settings.flying = False

    if settings.game_over == False and settings.flying == True:
        # Generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - settings.last_pipe > settings.pipe_frequency:
            pipe_height = random.randint(-100, 100)
            bottom_pipe = Pipe(
                settings.WIDTH, int(settings.HEIGHT / 2) + pipe_height, -1, settings
            )
            top_pipe = Pipe(
                settings.WIDTH, int(settings.HEIGHT / 2) + pipe_height, 1, settings
            )
            pipe_group.add(bottom_pipe)
            pipe_group.add(top_pipe)
            settings.last_pipe = time_now
        bg_scroll -= bg_speed
        # Reset background to loop
        if abs(bg_scroll) > 105:
            bg_scroll = 0
        pipe_group.update()

    # Event Loop
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            run = False
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and settings.game_over == False
            and settings.flying == False
        ):
            settings.flying = True

    # Update Display
    pygame.display.update()

pygame.quit()
