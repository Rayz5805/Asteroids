import pygame
import sys
from constants import *
from text import Text
from asteroid import Asteroid, AsteroidField

def titles():
    pygame.init()
    pygame.display.set_caption("Asteroids")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    Asteroid.containers = (updatable, drawable)
    AsteroidField.containers = updatable
    Text.containers = (updatable, drawable)

    asteroid_field = AsteroidField()
    title_asteroid = Text(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 150, "ASTEROID")
    start_key = Text(SCREEN_WIDTH / 2, SCREEN_HEIGHT *2/3, 30, "Press K to start!")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_x]):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_k]:
                return

        updatable.update(dt)

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()

        dt = clock.tick(60) / 1000

