import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, text, pos, font):
        super().__init__()
        self.font = font
        self.text = text
        self.image = self.font.render(text, True, pygame.Color("White"))
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                print("Button clicked!")



