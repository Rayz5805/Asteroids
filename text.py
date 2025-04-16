import pygame
from constants import *

class Text():
    def __init__(self, x, y, text_size):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.x = x
        self.y = y
        self.font = pygame.font.SysFont("Arial", text_size)

    def draw(self, screen):
        pass

    def update(self, dt):
        pass

class Countdown():
    def __init__(self, timer, text_size):
        self.timer = timer
        self.text_size = text_size
        self.font = pygame.font.SysFont("Arial", text_size)

    def draw(self, screen):
        text = self.font.render(f"{round(self.timer, 1)}s", 1, "white")
        screen.blit(text, (SCREEN_WIDTH/2 - self.text_size/2, SCREEN_HEIGHT / 6))

    def update(self, dt):
        self.timer -= dt

    def add(self, dt):
        self.timer += 3