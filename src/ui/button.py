import pygame as pg


class Button:
    def __init__(self, x, y, image, single_click=True, check_mouse_on=False, center=False):
        self.image = image
        self.rect: pg.rect.Rect = self.image.get_rect()
        self.x = x
        self.y = y
        if center:
            self.rect.center = (x, y)
        else:
            self.rect.topleft = (x, y)
        self.clicked = True
        self.single_click = single_click
        self.check_mouse_on = check_mouse_on

    def draw(self, surface):
        mouse_clicked = False
        pos = pg.mouse.get_pos()

        if self.rect.collidepoint(pos):
            mouse_on = True
            if pg.mouse.get_pressed()[0] and not self.clicked:
                mouse_clicked = True
                if self.single_click:
                    self.clicked = True
        else:
            mouse_on = False

        if not pg.mouse.get_pressed()[0]:
            self.clicked = False

        surface.blit(self.image, self.rect)

        return (mouse_clicked, mouse_on) if self.check_mouse_on else mouse_clicked

    def change_image(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def change_pos(self, x, y, center=False):
        self.rect = self.image.get_rect()
        if center:
            self.rect.center = (x, y)
        else:
            self.rect.topleft = (x, y)
