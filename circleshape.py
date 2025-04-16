import pygame
from constants import *

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass

    def collideWith(self, other):
        distance = pygame.math.Vector2.distance_to(self.position, other.position)
        return self.radius + other.radius >= distance

    def checkOutOfBound(self):
        return (
            self.position.x > SCREEN_WIDTH * 1.5
            or self.position.x < -SCREEN_WIDTH * 0.5
            or self.position.y > SCREEN_HEIGHT * 1.5
            or self.position.y < -SCREEN_HEIGHT * 0.5
        )