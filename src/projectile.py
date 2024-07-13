import pygame


class Projectile:
    def __init__(self, position, target, cell_size, speed=5, damage=10):
        self.position = pygame.Vector2(position)
        self.target = target
        self.aim_point = target
        self.cell_size = cell_size
        self.color = (255, 51, 51)
        self.border_color = (255, 255, 255)  # Black border color
        self.border_width = 1  # Border width
        self.speed = speed
        self.damage = damage
        self.range = 120
        self.alive = True
        self.total_distance_traveled = 0

    def update(self, dt):
        if not self.alive:
            return

        if not self.target.alive:
            direction = (pygame.Vector2(self.aim_point.position) * self.cell_size - self.position).normalize()
            distance_traveled = direction * self.speed
            self.position += distance_traveled
        else:
            direction = (pygame.Vector2(self.target.position) * self.cell_size - self.position).normalize()
            distance_traveled = direction * self.speed
            self.position += distance_traveled

        self.total_distance_traveled += distance_traveled.length()

        if self.position.distance_to(pygame.Vector2(self.target.position) * self.cell_size) < self.speed:
            self.hit_target()

    def render(self, screen):
        if self.alive:
            center = self.find_unit_center()
            cell_rect = pygame.Rect(
                self.position.x,
                self.position.y,
                self.cell_size,
                self.cell_size
            )
            pygame.draw.circle(screen, self.color, center, self.cell_size)
            pygame.draw.rect(screen, self.border_color, cell_rect, self.border_width)

    def find_unit_center(self):
        x, y = self.position
        center_x = x + self.cell_size / 2
        center_y = y + self.cell_size / 2
        return int(center_x), int(center_y)

    def hit_target(self):
        self.target.take_damage(self.damage)
        self.alive = False

    def get_distance_traveled(self):
        return self.total_distance_traveled / self.cell_size
