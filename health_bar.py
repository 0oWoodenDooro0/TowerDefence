import pygame.draw


class HealthBar:
    def __init__(self, x, y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp

    def draw(self, surface):
        if self.hp == self.max_hp: return
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, "red", (self.x - self.w // 2, self.y + 15, self.w, self.h))
        pygame.draw.rect(surface, "green", (self.x - self.w // 2, self.y + 15, self.w * ratio, self.h))

    def update(self, x, y, hp):
        self.x = x
        self.y = y
        self.hp = hp
