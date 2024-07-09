import sys


from states.basestate import BaseState


import pygame
from map import Map
from tower import Tower
from unit import Unit


class PlayState(BaseState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.map = Map(100, 100, 10)
        self.paths = [self.map.generate_path((x, 0), (x, 99), 10) for x in range(25)]
        self.units = [
            Unit(self.paths[x]) for x in range(25)
        ]
        self.towers = [
            Tower((15, 70), 10)
        ]

    def handle_event(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print((mouse_x, mouse_y))
                print((mouse_x // 10, mouse_y // 10))
                self.map.toggle_square(mouse_x // 10, mouse_y // 10)
                for unit in self.units:
                    unit.handle_click()

    def update(self):
        self.units = [unit for unit in self.units if unit.alive or (unit.explosion and not unit.explosion.is_finished())]

        for unit in self.units:
            unit.update()

        for tower in self.towers:
            tower.update(self.units)

    def render(self, screen):
        screen.fill((0, 0, 0))

        self.map.render(screen)

        for unit in self.units:
            unit.render(screen)

        for tower in self.towers:
            tower.render(screen)

        pygame.display.flip()
