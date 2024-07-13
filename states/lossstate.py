import pygame


from states.basestate import BaseState
from src.text import Text
from globals import G_OPTIONS


class LossState(BaseState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.loss_text = Text('You Lose.', 55, 'white', (G_OPTIONS['display']['width'] // 2, G_OPTIONS['display']['height'] // 2))
        self.font = pygame.font.SysFont(None, 55)
        self.text = "Loser"
        self.text_color = (255, 255, 255)  # White

        # Render the text
        self.text_surface = self.font.render(self.text, True, self.text_color)

        # Get the rectangle of the text surface
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = (400, 300)  # Center the text in the middle of the screen

    def update(self, dt):
        pass

    def render(self, screen):
        screen.fill((0, 0, 0))

        screen.blit(self.text_surface, self.text_rect)
        pygame.draw.rect(screen, (255, 0, 0), self.text_rect.inflate(20, 20),
                         2)  # Red rectangle with padding and width of 2

        pygame.display.flip()

    def handle_event(self, events):
        if events.type == pygame.MOUSEBUTTONDOWN:
            self.state_manager.change('deploy')


