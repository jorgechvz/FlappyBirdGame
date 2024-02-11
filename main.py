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

# Styles and Fonts
font = pygame.font.SysFont("Verdana", 60)
white = (255, 255, 255)

# Set background image and scale it to fit the screen
bg_sky_image = pygame.image.load("assets/fb-background.png").convert()
bg_sky_image = pygame.transform.scale(bg_sky_image, (settings.WIDTH, settings.HEIGHT))
bg_ground_image = pygame.image.load("assets/fb-ground.png").convert()
button_img = pygame.image.load("assets/fb-restart.png").convert()
title_img = pygame.image.load("assets/fb-title.png").convert_alpha()
title_img = pygame.transform.scale(title_img, (500, 200))
start_img = pygame.image.load("assets/fb-start.png").convert_alpha()
start_img = pygame.transform.scale(start_img, (200, 100))
game_over_img = pygame.image.load("assets/fb-game-over.png").convert_alpha()
game_over_img = pygame.transform.scale(game_over_img, (500, 200))


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
    settings.score = 0
    return settings.score


def draw_score_message():
    # Calculate the size of the text
    text = "Score: " + str(settings.score)
    text_size = font.size(text)

    # Calculate the x and y coordinates of the rectangle and the text
    rect_x = settings.WIDTH / 2 - text_size[0] / 2 - 5
    rect_y = settings.HEIGHT / 2 - text_size[1] / 2 - 5
    text_x = settings.WIDTH / 2 - text_size[0] / 2
    text_y = settings.HEIGHT / 2 - text_size[1] / 2

    # Draw a mustard rectangle that is a bit larger than the text size
    pygame.draw.rect(
        screen, (227, 207, 87), (rect_x, rect_y, text_size[0] + 10, text_size[1] + 10)
    )

    # Draw the text on top of the rectangle at the adjusted coordinates
    draw_text(text, font, white, text_x, text_y)


# Create a restart button
restart_button = Button(
    settings.WIDTH // 2 - 50, settings.HEIGHT // 2 + 200, button_img
)
next_level_button = Button(settings.WIDTH / 2, settings.HEIGHT / 2, button_img)
show_message = True

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

    # Logic for score
    if len(pipe_group) > 0:
        for pipe in pipe_group:
            if pipe.position == -1:  # Only score for bottom pipes
                if (
                    bird_group.sprites()[0].rect.left > pipe.rect.left
                    and bird_group.sprites()[0].rect.right < pipe.rect.right
                ):
                    pipe.passed_pipe = True
                if pipe.passed_pipe == True:
                    if bird_group.sprites()[0].rect.left > pipe.rect.right:
                        settings.point_sound.play()
                        settings.score += 1
                        pipe.passed_pipe = False
    # Display Score
    if show_message:
        screen.blit(title_img, (settings.WIDTH / 2 - title_img.get_width() / 2, 100))
        screen.blit(start_img, (settings.WIDTH / 2 - start_img.get_width() / 2, 600))

    if settings.game_over == False and show_message == False:
        draw_text(str(settings.score), font, white, int(settings.WIDTH / 2), 40)

    if not settings.game_over and (
        pygame.sprite.groupcollide(bird_group, pipe_group, False, False)
        or flappy_bird.rect.top < 0 or flappy_bird.rect.bottom > 682
    ):
        settings.hit_sound.play()
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
        pipe_group.update()
        bg_scroll -= bg_speed
        # Reset background to loop
        if abs(bg_scroll) > 105:
            bg_scroll = 0

    if settings.game_over == True:
        screen.blit(
            game_over_img, (settings.WIDTH / 2 - game_over_img.get_width() / 2, 100)
        )
        draw_score_message()
        if restart_button.draw(screen) == True:
            settings.game_over = False
            show_message = True
            settings.score = reset_game()

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
            show_message = False

    # Update Display
    pygame.display.update()

pygame.quit()
