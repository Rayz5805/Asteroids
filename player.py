import pygame
from circleshape import CircleShape
from text import Text, Instruction
from shot import Shot
from constants import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.hitless_timer = 0
        self.survive_time = 0
        self.life = PLAYER_LIFE
    
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, surface):
        if not self.able_collision and round(self.survive_time * 10) % 2 == 1:
            return
        pygame.draw.polygon(surface, "white", self.triangle(), 2)
        life_display = Text(self.position.x, self.position.y + 30, 20, f"x {self.life}")
        life_display.draw(surface)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def stayInBound(self, dt):
        if self.position.x > SCREEN_WIDTH:
            self.position.x -= PLAYER_SPEED * dt
        if self.position.x < 0:
            self.position.x += PLAYER_SPEED * dt
        if self.position.y > SCREEN_HEIGHT:
            self.position.y -= PLAYER_SPEED * dt
        if self.position.y < 0:
            self.position.y += PLAYER_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.shoot_timer -= dt
        self.hitless_timer -= dt
        self.survive_time += dt
        self.stayInBound(dt)

        if self.hitless_timer <= 0:
            self.able_collision = True

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def getHit(self):
        self.life -= 1
        self.hitless_timer = PLAYER_HITLESS_COOLDOWN
        self.able_collision = False

    def death(self):
        self.kill()
        gameOver = Text(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3, 100, "GAME OVER")
        subtext = Text(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, 30, f"You've survived for {round(self.survive_time, 1)}s")
        instuction = Instruction(SCREEN_WIDTH / 2, SCREEN_HEIGHT *2/3, 20, "Press R to restart")
        return gameOver, subtext, instuction
        

