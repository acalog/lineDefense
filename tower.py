import pygame
import math

from projectile import Projectile


class Tower:
    def __init__(self, position, cell_size, range=10000, damage=30, fire_rate=5):
        self.position = position
        self.range = range
        self.cell_size = cell_size
        self.cell_color = (51, 255, 153)
        self.damage = damage
        self.fire_rate = fire_rate
        self.cooldown = 0
        self.projectiles = []

    def update(self, enemies):
        if self.cooldown > 0:
            self.cooldown -= 1

        if self.cooldown == 0:
            target = self.find_target(enemies)
            if target:
                self.shoot(target)
                self.cooldown = self.fire_rate

        for projectile in self.projectiles:
            projectile.update()

        # Remove projectiles that are no longer alive
        self.projectiles = [p for p in self.projectiles if p.alive]

    def find_target(self, enemies):
        closest_enemy = None
        closest_distance = float('inf')

        for enemy in enemies:
            enemy_position = pygame.Vector2(enemy.position) * enemy.cell_size
            tower_position = pygame.Vector2(self.position) * self.cell_size
            distance = tower_position.distance_to(enemy_position)

            if distance <= self.range and distance < closest_distance:
                closest_distance = distance
                closest_enemy = enemy

        return closest_enemy

    def shoot(self, target):
        projectile_position = (self.position[0] * self.cell_size + self.cell_size // 2, self.position[1] * self.cell_size + self.cell_size // 2)
        projectile = Projectile(projectile_position, target, 10, speed=5, damage=self.damage)
        self.projectiles.append(projectile)

    def render(self, screen):
        x, y = self.position
        pygame.draw.rect(screen, self.cell_color, pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

        for projectile in self.projectiles:
            projectile.render(screen)
