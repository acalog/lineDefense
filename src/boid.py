import random
import pygame


class Boid:
    def __init__(self, x, y):
        self.max_speed = 2
        self.max_force = 0.05
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acceleration = pygame.Vector2(0, 0)

    def update(self):
        self.velocity += self.acceleration
        self.velocity = self.velocity.normalize() * self.max_speed
        self.position += self.velocity
        self.acceleration *= 0
