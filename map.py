import random

import pygame
import math


class Map:
    def __init__(self, width, height, cell_size):
        self.colors = {
            'PATH': (255, 0, 0),
        }
        self.object_type = {
            'LAND': 0,
            'PATH': 2
        }
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = self.create_grid()
        # self.make_line(2, 4)
        # self.make_line(3, self.height - 20)
        # self.draw_path((4, 10), (4, self.height - 10))

    def create_grid(self):
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(0)
            grid.append(row)
        return grid

    def render(self, screen):
        color = (0, 255, 0)
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] == self.object_type['LAND']:
                    color = (103, 114, 91)
                elif self.grid[y][x] == self.object_type['PATH']:
                    color = self.colors['PATH']
                elif self.grid[y][x] == 3:
                    color = (0, 0, 255)
                pygame.draw.rect(screen, color,
                                 pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

    def place(self, object_type, x, y):
        self.grid[y][x] = object_type

    def make_line(self, object_type, y):
        for x in range(self.width):
            self.place(object_type, x, y)

    def move_towards(self, start, end, speed):
        x0, y0 = start
        x1, y1 = end

        # Calculate the distance
        distance = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

        # Check if we are already at the target
        if distance == 0:
            return end

        # Calculate the unit vector (direction)
        direction_x = (x1 - x0) / distance
        direction_y = (y1 - y0) / distance

        # Calculate new position
        new_x = x0 + direction_x * speed
        new_y = y0 + direction_y * speed

        # Check if the new position overshoots the target
        if math.sqrt((x1 - new_x) ** 2 + (y1 - new_y) ** 2) < speed:
            return end

        return (new_x, new_y)

    def generate_path(self, start, end, speed):
        current_position = start
        path = [start]

        while current_position != end:
            current_position = self.move_towards(current_position, end, speed)
            path.append(current_position)

        return path

    def generate_random_path(self, start, end, speed):
        stack = [start]
        path = set()
        path.add(start)
        self.place(self.object_type['PATH'], int(start[0]), int(start[1]))

        while stack:
            current = stack[-1]

            if current == end:
                break

            neighbors = self.get_neighbors(current)
            random.shuffle(neighbors)

            moved = False
            for neighbor in neighbors:
                if neighbor not in path:
                    path.add(neighbor)
                    stack.append(neighbor)
                    self.place(self.object_type['PATH'], int(neighbor[0]), int(neighbor[1]))
                    moved = True
                    break

            if not moved:
                stack.pop()

        return list(path)

    def get_neighbors(self, pos):
        x, y = pos
        neighbors = []
        if x > 0:
            neighbors.append((x - 1, y))
        if x < self.width - 1:
            neighbors.append((x + 1, y))
        if y > 0:
            neighbors.append((x, y - 1))
        if y < self.height - 1:
            neighbors.append((x, y + 1))
        return neighbors

    def draw_random_path(self, start, end):
        path = self.generate_random_path(start, end, 1)
        for p in path:
            x, y = p
            self.place(self.object_type['PATH'], int(x), int(y))

    def draw_path(self, start, end):
        path = self.generate_path(start, end, 1)
        for p in path:
            x, y = p
            self.place(self.object_type['PATH'], int(x), int(y))

    def print_grid(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == 0:
                    print(f"({y}, {x})", end=' ')
                elif self.grid[y][x] == 2:
                    print(f"(E)", end=' ')
                elif self.grid[y][x] == 3:
                    print(f"(P)", end=' ')
            print()

    def toggle_square(self, x, y):
        self.grid[y][x] = 3
