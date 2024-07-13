import sys
import pygame


from src.statemachine import StateMachine
from states.deploystate import DeployState
from states.lossstate import LossState
from states.playstate import PlayState
from states.startstate import StartState
from states.victorystate import VictoryState

from globals import G_OPTIONS


class Game:
    def __init__(self):
        pygame.init()
        self.state_manager = StateMachine({
            'start': lambda: StartState(self.state_manager),
            'play': lambda: PlayState(self.state_manager),
            'victory': lambda: VictoryState(self.state_manager),
            'loss': lambda: LossState(self.state_manager),
            'deploy': lambda: DeployState(self.state_manager)
        })
        self.screen = pygame.display.set_mode(G_OPTIONS['display']['screen_size'])
        self.clock = pygame.time.Clock()
        self.fps = G_OPTIONS['display']['fps']
        self.dt = 0
        self.running = True

    def run(self):
        self.state_manager.change('deploy')
        while self.running:
            self.handle_events()
            self.update(self.dt)
            self.render()
            self.dt = self.clock.tick(60) * 0.1

        pygame.quit()
        sys.exit()

    def update(self, dt):
        self.state_manager.update(dt)

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.state_manager.handle_event(events=event)

    def render(self):
        self.state_manager.render(self.screen)
