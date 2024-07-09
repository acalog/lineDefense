import pygame


class Projectile:
    def __init__(self, position, target, cell_size, speed=5, damage=10):
        self.position = pygame.Vector2(position)
        self.target = target
        self.cell_size = cell_size
        self.color = (255, 51, 51)
        self.speed = speed
        self.damage = damage
        self.alive = True

    def update(self):
        if not self.alive:
            return

        direction = (pygame.Vector2(self.target.position) * self.cell_size - self.position).normalize()
        self.position += direction * self.speed

        if self.position.distance_to(pygame.Vector2(self.target.position) * self.cell_size) < self.speed:
            if not self.target.alive:
                self.alive = False
                return
            self.hit_target()

    def render(self, screen):
        if self.alive:
            pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), 5)

    def hit_target(self):
        self.target.take_damage(self.damage)
        self.alive = False