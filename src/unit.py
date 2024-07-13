import pygame

from src.explosion import Explosion
from src.healthbar import HealthBar
from globals import G_OPTIONS


class Unit:
    def __init__(self, path, size, health, speed):
        self.position_index = 0
        self.path = path
        self.position = self.path[self.position_index]
        self.speed = speed
        self.cell_size = size
        self.cell_color = (35, 73, 136)
        self.border_color = (0, 0, 0)  # Black border color
        self.border_width = 1  # Border width

        self.paused = False
        self.alive = True
        self.max_health = health
        self.health = self.max_health
        self.health_percent = 1
        self.explosion = None
        self.health_bar = HealthBar()
        self.bouncing = False

    def update(self, dt):
        if not self.alive:
            if self.explosion:
                self.explosion.update()
            return
        if self.paused:
            self.do_action('pause')
        else:
            self.do_action('move', dt)

        self.health_bar.update(self.health_percent)

    def do_action(self, action, params=None):
        action = getattr(self, action)
        action(params)

    def move(self, dt):
        """
        if self.position_index < len(self.path) - 1:
            current_pos = pygame.Vector2(self.position[0] * self.cell_size, self.position[1] * self.cell_size)
            next_pos = pygame.Vector2(self.path[self.position_index + 1][0] * self.cell_size, self.path[self.position_index + 1][1] * self.cell_size)
            direction = (next_pos - current_pos).normalize()
            current_pos += direction * self.speed
            if current_pos.distance_to(next_pos) < self.speed:
                self.position_index += 1
            self.position = (current_pos.x / self.cell_size, current_pos.y / self.cell_size)
            print(self.position)
        else:
            self.position_index = 0
            self.position = self.path[self.position_index]
        """
        if self.position_index >= len(self.path) - 1:
            return  # Reached the end of the path

        current_pos = pygame.Vector2(self.position[0] * self.cell_size,
                                     self.position[1] * self.cell_size)
        next_pos = pygame.Vector2(self.path[self.position_index + 1][0] * self.cell_size,
                                  self.path[self.position_index + 1][1] * self.cell_size)
        # print('Current position {} - Next position ({}, {})'.format(self.position, next_pos[0] / self.cell_size, next_pos[1] / self.cell_size))
        direction = (next_pos - current_pos).normalize()
        # print('Direction {}'.format(direction))
        current_pos += direction * self.speed

        if current_pos.distance_to(next_pos) < self.speed:
            self.position_index += 1

        self.position = (current_pos.x / self.cell_size, current_pos.y / self.cell_size)

    def pause(self, dt):
        pass

    def render(self, screen):
        if self.alive:
            center = self.find_unit_center()

            # if self.bouncing:
            #     pygame.draw.circle(screen, (0, 255, 0), center, self.cell_size)
            # elif self.health == 60:
            #     self.cell_color = self.bar_color # self.cell_color = (red, green, blue)
            # else:
            #     self.cell_color = self.health_bar['DAMAGED']
            rgb = (self.health_bar.get_red(), self.health_bar.get_green(), self.health_bar.get_blue())
            self.cell_color = rgb
            cell_rect = pygame.Rect(
                self.position[0] * self.cell_size,
                self.position[1] * self.cell_size,
                self.cell_size,
                self.cell_size
            )

            pygame.draw.circle(screen, self.cell_color, center, self.cell_size)
            pygame.draw.rect(screen, self.border_color, cell_rect, self.border_width)

        elif self.explosion:
            self.explosion.render(screen)

    def handle_click(self):
        if self.paused is False:
            self.paused = True
        else:
            self.paused = False

    def take_damage(self, damage):
        self.health -= damage
        self.health_percent = self.health / self.max_health
        # print("Health percent left: {}".format(self.health_percent))
        if self.health <= 0:
            self.alive = False
            self.explosion = Explosion(self.position, self.cell_size)

    def find_unit_center(self):
        """Calculates the pixel coordinates of the center of the cell."""
        x, y = self.position
        center_x = x * self.cell_size + self.cell_size / 2
        center_y = y * self.cell_size + self.cell_size / 2
        return int(center_x), int(center_y)

    def check_collision(self, other):
        # print(pygame.Vector2(self.position).distance_to(pygame.Vector2(other.position)) * self.cell_size)
        return pygame.Vector2(self.position).distance_to(pygame.Vector2(other.position)) < self.cell_size / self.cell_size

    def bounce_off(self, other):
        current_pos = pygame.Vector2(self.position[0] * self.cell_size,
                                     self.position[1] * self.cell_size)
        other_pos = pygame.Vector2(other.position[0] * self.cell_size,
                                   other.position[1] * self.cell_size)
        direction = (current_pos - other_pos).normalize()
        current_pos += direction * self.speed * 2  # Move in the opposite direction
        # print(self.position)
        self.position = (current_pos.x / self.cell_size, current_pos.y / self.cell_size)
