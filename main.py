import pygame
import sys
from constants import *
from player import Player
from shot import Shot
from asteroid import Asteroid, AsteroidField
from text import Countdown

def handleAsteroidCollision(asteroid, player, countdown):
    if asteroid.checkTooOutOfBound():
        asteroid.kill()
    
    if asteroid.collideWith(player):
        if player.life > 1:
            player.getHit() 
        else:
            countdown.kill()
            asteroid.split()
            return player.death()
        
def handleShotCollision(shot, asteroid, countdown):
    if shot.checkTooOutOfBound():
        shot.kill()

    if asteroid.collideWith(shot):
        shot.kill()
        asteroid.split()
        countdown.addTime()##
    


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
    asteroid_field = AsteroidField()
    countdown = Countdown(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 6, 40, "")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_x]:
                return

        if countdown.timer <= 0:
            drawable.add(player.death())
            countdown.kill()

        updatable.update(dt)

        screen.fill("black")

        for asteroid in asteroids:
            death_message = handleAsteroidCollision(asteroid, player, countdown)
            if death_message:
                drawable.add(death_message)

            for shot in shots:
                handleShotCollision(shot, asteroid, countdown)
    
        for obj in drawable:
            obj.draw(screen)
        
        pygame.display.flip()

        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()