import pygame
from constants import *
from player import Player
from shot import Shot
from asteroid import Asteroid, AsteroidField
from text import Countdown, Instruction

def game():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    scanline_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    for y in range(0, SCREEN_HEIGHT, 4):
        pygame.draw.line(scanline_surface, (100,100,100,50), (0, y), (SCREEN_WIDTH, y))
    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)
    Countdown.containers = (updatable, drawable)
    Instruction.containers = (updatable, drawable)

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

    dt = 0
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    asteroid_field = AsteroidField()
    countdown = Countdown(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 6, 40, "")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_x]):
                running = False
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_r]:
                game()
                return

        if countdown.timer <= 0:
            drawable.add(player.death())
            countdown.kill()

        updatable.update(dt)

        surface.fill((20,20,20,))
        screen.fill("black")

        for asteroid in asteroids:
            death_message = handleAsteroidCollision(asteroid, player, countdown)
            if death_message:
                drawable.add(death_message)

            for shot in shots:
                handleShotCollision(shot, asteroid, countdown)
    
        for obj in drawable:
            obj.draw(surface)
        surface.blit(scanline_surface, (0,0))
        screen.blit(surface, (0,0))
        
        pygame.display.flip()

        dt = clock.tick(60) / 1000