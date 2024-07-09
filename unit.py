import pygame

from explosion import Explosion


class Unit:
    def __init__(self, path):
        self.position_index = 0
        self.path = path
        self.position = self.path[self.position_index]
        self.speed = 0.25
        self.cell_size = 10
        self.cell_color = (35, 73, 136)
        self.paused = False
        self.alive = True
        self.health = 60
        self.explosion = None
        self.health_bar = {
            'FULL': (35, 73, 136),
            'DAMAGED': (255, 255, 0)
        }

    def update(self):
        if not self.alive:
            if self.explosion:
                self.explosion.update()
            return
        if self.paused:
            self.do_action('pause')
        else:
            self.do_action('move')

    def do_action(self, action):
        action = getattr(self, action)
        action()

    def move(self):
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

        current_pos = pygame.Vector2(self.position[0] * self.cell_size, self.position[1] * self.cell_size)
        next_pos = pygame.Vector2(self.path[self.position_index + 1][0] * self.cell_size,
                           self.path[self.position_index + 1][1] * self.cell_size)
        direction = (next_pos - current_pos).normalize()
        current_pos += direction * self.speed

        if current_pos.distance_to(next_pos) < self.speed:
            self.position_index += 1

        self.position = (current_pos.x / self.cell_size, current_pos.y / self.cell_size)

    def pause(self):
        pass

    def render(self, screen):
        if self.alive:
            center = self.find_unit_center()
            if self.health == 60:
                self.cell_color = self.health_bar['FULL']
            else:
                self.cell_color = self.health_bar['DAMAGED']
            pygame.draw.circle(screen, self.cell_color, center, self.cell_size)
        elif self.explosion:
            self.explosion.render(screen)

    def handle_click(self):
        if self.paused is False:
            self.paused = True
        else:
            self.paused = False

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            self.explosion = Explosion(self.position, self.cell_size)

    def find_unit_center(self):
        """Calculates the pixel coordinates of the center of the cell."""
        x, y = self.position
        center_x = x * self.cell_size + self.cell_size / 2
        center_y = y * self.cell_size + self.cell_size / 2
        return int(center_x), int(center_y)


