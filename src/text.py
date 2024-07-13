import pygame


from src.palette import Palette


class Text:
    """
        Text to display on screen.
            text   - text to display
            font   - font size
            color  - font color
            center - where to render the text on screen. Tuple of pixel values
    """
    def __init__(self, text, font, color, center):
        self.palette = Palette()
        self.font = pygame.font.SysFont(None, font)
        self.text = text
        self.color = self.palette.get(color)
        self.text_surface = self.font.render(self.text, True, self.color)
        # Get the rectangle of the text surface
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.center = center

    def render(self, screen):
        screen.blit(self.text_surface, self.text_rect)

    def set_text(self, text):
        self.text = text
        self.text_surface = self.font.render(self.text, True, self.color)



