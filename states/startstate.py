import sys


from states.basestate import BaseState


import pygame


class StartState(BaseState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.font = pygame.font.SysFont(None, 55)
        self.text = "Hello, Pygame!"
        self.text_color = (255, 255, 255)  # White

        # Render the text
        self.text_surface = self.font.render(self.text, True, self.text_color)

        # Get the rectangle of the text surface
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = (400, 300)  # Center the text in the middle of the screen

    def handle_event(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.state_manager.change('play')

                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos)
                # Check if the text or image is clicked
                if self.text_rect.collidepoint(mouse_pos):
                    self.state_manager.change('play')


    def render(self, screen):
        screen.fill((0, 0, 0))

        screen.blit(self.text_surface, self.text_rect)
        pygame.draw.rect(screen, (255, 0, 0), self.text_rect.inflate(20, 20), 2)  # Red rectangle with padding and width of 2

        pygame.display.flip()


