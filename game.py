import sys
import pygame

from states.playstate import PlayState
from states.startstate import StartState
from statemachine import StateMachine


class Game:
    def __init__(self):
        pygame.init()
        self.state_manager = StateMachine({
            'start': lambda: StartState(self.state_manager),
            'play': lambda: PlayState(self.state_manager)
        })
        self.screen = pygame.display.set_mode((1000, 1000))
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        self.state_manager.change('start')
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def update(self):
        self.state_manager.update()

    def handle_events(self):
        self.state_manager.handle_event(events=pygame.event.get())

    def render(self):
        self.state_manager.render(self.screen)
        """
        self.screen.fill((0, 0, 0))

        self.map.render(self.screen)

        for unit in self.units:
            unit.render(self.screen)

        for tower in self.towers:
            tower.render(self.screen)

        pygame.display.flip()
        """

