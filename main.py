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
    texts = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)
    Countdown.containers = (texts, updatable, drawable)


    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    asteroid_Field = AsteroidField()
    countdown = Countdown(SCREEN_WIDTH / 2 - 40, SCREEN_HEIGHT / 6, 40, "")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        if countdown.timer <= 0:
            player.death()

        updatable.update(dt)

        screen.fill("black")

        for asteroid in asteroids:
            if asteroid.collideWith(player):
                drawable.add(player.death())
                countdown.kill()
                asteroid.split()

            if asteroid.checkOutOfBound():
                asteroid.kill()

            for shot in shots:
                if asteroid.collideWith(shot):
                    shot.kill()
                    asteroid.split()
                    countdown.addTime()

                if shot.checkOutOfBound():
                    shot.kill()
    
        for obj in drawable:
            obj.draw(screen)
        
        pygame.display.flip()

        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()