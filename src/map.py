import random
import pygame
import math


from src.palette import Palette
from globals import G_OPTIONS


class Map:
    def __init__(self, width, height, cell_size):
        self.colors = Palette()
        self.object_type = {
            'SKY': 0,
            'LAND': 1,
            'PATH': 2,
        }
        # Columns
        self.width = width
        # Rows
        self.height = height
        self.cell_size = cell_size
        self.grid = self.create_grid()
        self.enemy_spawn_zone = G_OPTIONS['game']['enemy_spawn_boundary']
        # self.make_line(2, 4)
        # self.make_line(3, self.height - 20)
        # self.draw_path((4, 10), (4, self.height - 10))

    def create_grid(self):
        """
        Creates a grid initialized with zeros.

        This method generates a 2D grid (a list of lists) based on the instance's height and
        width attributes. Each cell in the grid is initialized to 0.

        :return: A 2D grid (list of lists) with dimensions [height][width], where each cell is initialized to 0.
        :rtype: list of list of int
        """
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if y >= self.height - 5:
                    row.append(1)
                else:
                    row.append(0)
            grid.append(row)
        return grid

    def render(self, screen):
        color = self.colors.get('green')
        # Iterate through rows
        for y in range(self.height):
            # Iterate through columns
            for x in range(self.width):
                if self.grid[y][x] == self.object_type['SKY']:
                    color = self.colors.get('SKY')  # color = (103, 114, 91)
                elif self.grid[y][x] == self.object_type['PATH']:
                    color = self.colors.get('land green')
                elif self.grid[y][x] == 3:
                    color = self.colors.get('green')
                elif self.grid[y][x] == self.object_type['LAND']:
                    color = self.colors.get('LAND')
                pygame.draw.rect(screen, color,
                                 pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

    def place(self, object_type, x, y):
        """
            Places an object of a specified type at a given position on the grid.

            This method sets the value at the specified (x, y) position on the grid
            to the given object type.

            :param object_type: The type of object to place on the grid. This should correspond
                                to a valid object type defined in the instance.
            :type object_type: Any
            :param x: The x-coordinate (column index) where the object should be placed.
            :type x: int
            :param y: The y-coordinate (row index) where the object should be placed.
            :type y: int
            """
        self.grid[y][x] = object_type

    def make_line(self, object_type, y):
        for x in range(self.width):
            self.place(object_type, x, y)

    def move_towards(self, start, end, speed):
        """
            Moves from the start point towards the end point by a specified speed.

            This method calculates a new position by moving from the start point towards
            the end point. It ensures that the movement does not overshoot the end point.

            :param start: The starting point as a tuple (x, y).
            :type start: tuple of (float, float)
            :param end: The end point as a tuple (x, y).
            :type end: tuple of (float, float)
            :param speed: The distance to move from the start point towards the end point.
            :type speed: float
            :return: A new position as a tuple (x, y) after moving towards the end point by the specified speed.
            :rtype: tuple of (float, float)
        """
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

        return new_x, new_y

    def generate_path(self, start, end, speed=10):
        """
        Generates a path from the start point to the end point, moving at a specified speed.

        This method computes a list of positions from the start to the end by moving towards
        the end point incrementally, based on the given speed. It continuously updates the
        current position until it reaches the end point

        :param start: The starting point of the path. It should be a coordinate or position
                      that is understood by the `move_towards` method
        :type start: Any
        :param end: The end point of the path. It should be a coordinate or position
                    that is understood by the `move_towards` method
        :type end: Any
        :param speed: The speed at which to move from start to end. It determines the
                      incremental steps taken towards the end point. Defaults to 10
        :type speed: int, optional
        :return: A list of positions representing the path from start to end.
        :rtype: list
        """
        current_position = start
        path = [start]

        while current_position != end:
            current_position = self.move_towards(current_position, end, speed)
            path.append(current_position)

        return path

    def generate_random_path(self, start, end, speed):
        """
        Generates a random path from the start point to the end point.

        This method uses a depth-first search (DFS) algorithm to generate a random path from
        the start point to the end point. It places path markers on the grid as it progresses.

        :param start: The starting point of the path as a tuple (x, y).
        :type start: Any
        :param end: The end point of the path as a tuple (x, y).
        :type end: tuple of (int, int)
        :param speed: The speed parameter (currently not utilized in this method).
        :type speed: int
        :return: A list of tuples representing the points in the generated path.
        :rtype: list of (int, int)
        """
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
        if self.grid[y][x] < 3:
            self.grid[y][x] = 3
        else:
            self.grid[y][x] = 0

    def get_spawn_zone(self):
        return self.enemy_spawn_zone

    def get_cell(self, x, y):
        return self.grid[y][x]
