import pygame


from states.basestate import BaseState
from src.text import Text


class StartState(BaseState):
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.start_text = Text("Line Defense", 55, 'white', (400, 300))

    def handle_event(self, events):
        if events.type == pygame.MOUSEBUTTONDOWN:
            # self.state_manager.change('play')
            mouse_pos = pygame.mouse.get_pos()
            print(mouse_pos)
            # Check if the text or image is clicked
            if self.start_text.text_rect.collidepoint(mouse_pos):
                self.state_manager.change('deploy')


    def render(self, screen):
        screen.fill((0, 0, 0))

        self.start_text.render(screen)

        pygame.display.flip()


