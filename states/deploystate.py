import pygame

from states.basestate import BaseState
from src.map import Map
from src.text import Text
from globals import G_OPTIONS


class DeployState(BaseState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.map = Map(G_OPTIONS['map']['rows'], G_OPTIONS['map']['columns'], G_OPTIONS['map']['cell_size'])
        self.towers = {}
        self.towers_to_place = G_OPTIONS['game']['max_towers']
        self.ready_to_deploy = False
        self.text = Text('3 remaining', 55, 'red', (50 * G_OPTIONS['map']['cell_size'], 2 * G_OPTIONS['map']['cell_size']))
        self.start_text = Text('Ready', 55, 'red', (250, 50))

    def update(self, dt):
        if self.towers_to_place < 1:
            self.ready_to_deploy = True

    def render(self, screen):
        screen.fill((0, 0, 0))

        self.map.render(screen)

        self.text.render(screen)

        if self.ready_to_deploy:
            self.start_text.render(screen)

        pygame.display.flip()

    def handle_event(self, events):
        if events.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # print((mouse_x, mouse_y))
            print((mouse_x // 10, mouse_y // 10))
            x = mouse_x // 10
            y = mouse_y // 10
            position_key = "{}, {}".format(x, y)
            position_cell = self.map.get_cell(x, y)
            print(position_cell)
            if self.ready_to_deploy:
                if self.start_text.text_rect.collidepoint((mouse_x, mouse_y)):
                    params = {
                        'towers': self.towers
                    }
                    self.state_manager.change('play', enter_params=params)

            if self.map.get_cell(x, y) < 3:
                if self.towers_to_place > 0:

                    self.towers[position_key] = (x, y)
                    self.towers_to_place -= 1
                    self.map.toggle_square(x, y)

            else:
                self.towers_to_place += 1
                del self.towers[position_key]
                self.ready_to_deploy = False
                self.map.toggle_square(x, y)

            print("Towers to place {}".format(self.towers_to_place))
            self.text.set_text("{} remaining".format(self.towers_to_place))


