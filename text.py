import pygame
from constants import *

class Text(pygame.sprite.Sprite):
    def __init__(self, x, y, text_size, inputs):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = (x, y)
        self.text_size = text_size
        self.font = pygame.font.SysFont("Arial", text_size)
        self.inputs = inputs

    def draw(self, screen):
        text = self.font.render(self.inputs, 1, "white")
        screen.blit(text, self.position)

    def update(self, dt):
        pass

class Countdown(Text):
    def __init__(self, x, y, text_size, inputs):
        super().__init__(x, y, text_size, inputs)

        self.timer = GAME_COUNTDOWN

    def draw(self, screen):
        text = self.font.render(f"{round(self.timer, 1)}s", 1, "white")
        screen.blit(text, self.position)

    def update(self, dt):
        self.timer -= dt

    def addTime(self):
        self.timer += 1