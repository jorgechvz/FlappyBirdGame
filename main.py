import pygame
from pygame.locals import *

# Flappy Bird Game Main File
pygame.init()

# Game Variables
WIDTH = 864
HEIGHT = 936
CLOCK = pygame.time.Clock()
FPS = 60

# Game Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Scroll Background
bg_scroll = 0
bg_speed = 4

# Set background image and scale it to fit the screen
bg_sky_image = pygame.image.load('assets/fb-background.png').convert()
bg_sky_image = pygame.transform.scale(bg_sky_image, (WIDTH, HEIGHT))
bg_groudn_image = pygame.image.load('assets/fb-ground.png').convert()

run = True
while run:
    CLOCK.tick(FPS)
    
    # Draw background image
    screen.blit(bg_sky_image, (0, 0))
    screen.blit(bg_groudn_image, (bg_scroll, 682))
    
    bg_scroll -= bg_speed
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    pygame.display.update()
            
pygame.quit()            