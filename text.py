import pygame
from constants import *

class Text(pygame.sprite.Sprite):
    def __init__(self, x, y, text_size, inputs):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.x = x
        self.y = y
        self.text_size = text_size
        self.font = pygame.font.SysFont("consolas", text_size)
        self.inputs = inputs

    def draw(self, surface):
        text = self.font.render(self.inputs, 1, "white")
        surface.blit(text, (self.x - text.get_width()/2, self.y - text.get_height()/2))

    def update(self, dt):
        pass

class Countdown(Text):
    def __init__(self, x, y, text_size, inputs):
        super().__init__(x, y, text_size, inputs)

        self.timer = GAME_COUNTDOWN

    def draw(self, surface):
        if self.timer < 5 and round(self.timer * 9) % 3 == 0:
            return
        countdown_text = self.font.render(f"{round(self.timer, 1)}s", 1, "white")
        surface.blit(countdown_text, (self.x - countdown_text.get_width()/2, self.y - countdown_text.get_height()/2))

    def update(self, dt):
        self.timer -= dt

    def addTime(self):
        self.timer += 0.5

class Instruction(Text):
    def __init__(self, x, y, text_size, inputs):
        super().__init__(x, y, text_size, inputs)

        self.timer = 0

    def draw(self, surface):
        if round(self.timer * 2) % 2 == 0:
            return
        instuction_text = self.font.render(self.inputs, 1, "white")
        surface.blit(instuction_text, (self.x - instuction_text.get_width()/2, self.y - instuction_text.get_height()/2))

    def update(self, dt):
        self.timer += dt