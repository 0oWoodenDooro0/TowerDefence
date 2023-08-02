import pygame as pg


class Button:
    def __init__(self, x, y, image, single_click):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.single_click = single_click

    def draw(self, surface):
        action = False
        pos = pg.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] and not self.clicked:
                action = True
                if self.single_click:
                    self.clicked = True

        if not pg.mouse.get_pressed()[0]:
            self.clicked = False

        surface.blit(self.image, self.rect)

        return action