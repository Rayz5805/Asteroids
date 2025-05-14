import pygame
from constants import *
from asteroid import Asteroid, AsteroidField
from text import Text, Instruction

def menu():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    scanline_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    for y in range(0, SCREEN_HEIGHT, 4):
        pygame.draw.line(scanline_surface, (100,100,100,50), (0, y), (SCREEN_WIDTH, y))
    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    Asteroid.containers = (updatable, drawable)
    AsteroidField.containers = updatable
    Text.containers = drawable
    Instruction.containers = (updatable, drawable)

    #screen warp effect
    def warpBlit(screen, surface):
        for y in range(SCREEN_HEIGHT):
            slice_rect = pygame.Rect(0, y, SCREEN_WIDTH, 1)
            slice_img = surface.subsurface(slice_rect)
            curve_strenght = 0.0000008
            scale = 1 - curve_strenght * (y - SCREEN_HEIGHT/2) **2
            new_width = max(1, int(SCREEN_WIDTH * scale))
            offset = (SCREEN_WIDTH - new_width) //2
            scaled_slice = pygame.transform.scale(slice_img, (new_width , 1))

            screen.blit(scaled_slice, (offset, y))

    def tutorial():
        tutorial_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        tutorial_text = Text(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4, 50, "Tutorial on work, press DOWN key")

        pausing = True
        while pausing:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_DOWN]:
                    pausing = False
                    tutorial_text.kill()

            tutorial_surface.fill((0,0,0,200))
            tutorial_text.draw(tutorial_surface)

            for obj in drawable:
                obj.draw(surface)
            screen.blit(surface, (0,0))
            tutorial_surface.blit(scanline_surface, (0,0))
            screen.blit(tutorial_surface, (0,0))
            
            
            pygame.display.flip()
            clock.tick(30)



    dt = 0
    asteroid_field = AsteroidField()
    asteroid_text = Text(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 150, "ASTER0ID")

    start_text = Instruction(SCREEN_WIDTH / 2, SCREEN_HEIGHT *2/3, 30, "Press C to start!")
    tutorial_text = Instruction(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 8, 30, "Tutorial")
    up_text = Instruction(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 8 - 20, 30, "^")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_x]):
                return "quit"
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_c]:
                return "game"
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_UP]:
                tutorial()

        updatable.update(dt)
        
        surface.fill((20,20,20))
        screen.fill("black")

        for obj in drawable:
            obj.draw(surface)
        surface.blit(scanline_surface, (0,0))
        warpBlit(screen, surface)

        pygame.display.flip()

        dt = clock.tick(60) / 1000