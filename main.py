import pygame
import sys
from constants import *
from player import Player
from shot import Shot
from asteroid import Asteroid
from asteroidfield import AsteroidField
from text import Countdown

def main():
    pygame.init()
    pygame.display.set_caption("Asteroids")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)


    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    asteroid_Field = AsteroidField()
    countdown = Countdown(GAME_COUNTDOWN, 40)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        if countdown.timer <= 0:
            print("Game over!")
            sys.exit()

        updatable.update(dt)
        countdown.update(dt)

        screen.fill("black")

        countdown.draw(screen)

        for asteroid in asteroids:
            if asteroid.collideWith(player):
                print("Game over!")
                sys.exit()

            for shot in shots:
                if asteroid.collideWith(shot):
                    shot.kill()
                    asteroid.split()
                    countdown.add(dt)

        for obj in drawable:
            obj.draw(screen)
        pygame.display.flip()

        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()