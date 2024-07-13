import random

from states.basestate import BaseState


import pygame
from src.map import Map
from src.tower import Tower
from src.unit import Unit


from globals import G_OPTIONS


class PlayState(BaseState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.cell_size = G_OPTIONS['map']['cell_size']
        self.map = Map(G_OPTIONS['map']['rows'], G_OPTIONS['map']['columns'], self.cell_size)
        self.total_spawns = G_OPTIONS['game']['enemy_spawn_count']
        self.unit_settings = {
            'size': G_OPTIONS['map']['cell_size'],
            'health': G_OPTIONS['units']['max_health'],
            'speed': G_OPTIONS['units']['speed']
        }
        self.units = [
            self.spawn_unit() for x in range(self.total_spawns)
        ]
        self.towers = []
        self.loss_condition = self.map.height - 10

    def enter(self, params=None):
        tower_positions = params['towers']
        for position in tower_positions.values():
            self.towers.append(Tower(position, 10))

    def spawn_unit(self):
        starting_x = random.uniform(0, self.map.width - 1)
        starting_y = random.uniform(0, self.map.enemy_spawn_zone)
        target_x = random.uniform(0, self.map.width - 1)
        target_y = self.map.height - 2
        unit_path = self.map.generate_path((starting_x, starting_y), (target_x, target_y), 10)
        # unit_path = self.map.generate_random_path((starting_x, starting_y), (target_x, target_y), 10)
        # print(unit_path)
        return Unit(unit_path, self.unit_settings['size'], self.unit_settings['health'], self.unit_settings['speed'])

    def handle_event(self, events):
        if events.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # print((mouse_x, mouse_y))
            print((mouse_x // 10, mouse_y // 10))
            self.map.toggle_square(mouse_x // 10, mouse_y // 10)
            for unit in self.units:
                unit.handle_click()

    def update(self, dt):
        # Remove any dead units
        self.units = [unit for unit in self.units if unit.alive or (unit.explosion and not unit.explosion.is_finished())]

        for unit in self.units:
            # If unit's y-coord is greater than win condition line
            # enter victory state.
            if unit.position[1] > self.loss_condition:
                self.state_manager.change('loss')
            unit.update(dt)

        for tower in self.towers:
            tower.update(self.units, dt)
        if len(self.units) == 0:
            self.state_manager.change('victory')

    def render(self, screen):
        screen.fill((0, 0, 0))

        self.map.render(screen)

        for unit in self.units:
            unit.render(screen)

        # self.handle_collisions()

        for tower in self.towers:
            tower.render(screen)

        pygame.display.flip()

    def handle_collisions(self):
        for i, unit1 in enumerate(self.units):
            for j, unit2 in enumerate(self.units):
                if i != j and unit1.alive and unit2.alive and unit1.check_collision(unit2):
                    print("bouncing")
                    unit1.bounce_off(unit2)
                    unit2.bounce_off(unit1)
