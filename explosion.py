import random
import pygame


class Explosion:
    def __init__(self, position, cell_size, duration=30):
        self.position = pygame.Vector2(position)
        self.cell_size = cell_size
        self.duration = duration
        self.timer = 0
        self.particles = self.create_particles()

    def create_particles(self):
        particles = []
        for _ in range(40):
            particle_position = self.position + pygame.Vector2(random.uniform(-self.cell_size, self.cell_size),
                                                               random.uniform(-self.cell_size, self.cell_size))
            particle_velocity = pygame.Vector2(random.uniform(-2, 2), random.uniform(-2, 2))
            particles.append((particle_position, particle_velocity))
        return particles

    def update(self):
        self.timer += 1
        for i, (position, velocity) in enumerate(self.particles):
            position += velocity
            self.particles[i] = (position, velocity)

    def render(self, screen):
        for position, _ in self.particles:
            green = random.uniform(0, 150)
            pygame.draw.rect(screen, (255, green, 0),
                             (int(position.x * self.cell_size), int(position.y * self.cell_size), self.cell_size // 5, self.cell_size // 5))

    def is_finished(self):
        return self.timer >= self.duration
