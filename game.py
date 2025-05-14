import pygame
from constants import *
from player import Player
from shot import Shot
from asteroid import Asteroid, AsteroidField
from text import Text, Countdown, Instruction

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
    Text.containers = drawable
    Countdown.containers = (updatable, drawable)
    Instruction.containers = (updatable, drawable)

    def handleAsteroidCollision(asteroid, player, countdown):
        if asteroid.checkTooOutOfBound():
            asteroid.kill()
        
        if asteroid.collideWith(player) and player.life > 0:
            player.getHit() 
            if player.life < 1:
                countdown.kill()
                asteroid.split()
                drawable.add(player.death())
        
    def handleShotCollision(shot, asteroid, countdown):
        if shot.checkTooOutOfBound():
            shot.kill()

        if asteroid.collideWith(shot):
            shot.kill()
            asteroid.split()
            countdown.addTime()##

    def pause():
        pause_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        pause_text = Instruction(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 120, "Continue?")

        pausing = True
        while pausing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_x]):
                    pausing = False
                    return False
                if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_c]:
                    pausing = False
                    pause_text.kill()
                    return True

            pause_text.update(dt)
            pause_surface.fill((0,0,0,200))
            pause_text.draw(pause_surface)

            for obj in drawable:
                obj.draw(surface)
            screen.blit(surface, (0,0))
            pause_surface.blit(scanline_surface, (0,0))
            screen.blit(pause_surface, (0,0))
            
            
            pygame.display.flip()
            clock.tick(30)


    dt = 0
    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    asteroid_field = AsteroidField()
    countdown = Countdown(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 6, 40, "")

    #the game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_x]):
                running = pause()
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_r]:
                game()
                return False

        if countdown.timer <= 0:
            countdown.kill()
            drawable.add(player.death())

        updatable.update(dt)

        surface.fill((20,20,20))
        screen.fill("black")

        for asteroid in asteroids:
            handleAsteroidCollision(asteroid, player, countdown)

            for shot in shots:
                handleShotCollision(shot, asteroid, countdown)
    
        for obj in drawable:
            obj.draw(surface)
        surface.blit(scanline_surface, (0,0))
        screen.blit(surface, (0,0))
        
        pygame.display.flip()

        dt = clock.tick(60) / 1000
                