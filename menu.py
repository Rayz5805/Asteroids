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

    dt = 0
    asteroid_field = AsteroidField()
    title_asteroid = Text(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 150, "ASTER0ID")
    start_key = Instruction(SCREEN_WIDTH / 2, SCREEN_HEIGHT *2/3, 30, "Press K to start!")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_x]):
                return "quit"
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_k]:
                return "game"

        updatable.update(dt)
        
        surface.fill((20,20,20))
        screen.fill("black")

        for obj in drawable:
            obj.draw(surface)
        surface.blit(scanline_surface, (0,0))
        warpBlit(screen, surface)

        pygame.display.flip()

        dt = clock.tick(60) / 1000