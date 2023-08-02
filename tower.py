import math

import pygame as pg

import constants as c
from tower_data import TOWER_DATA


class Tower(pg.sprite.Sprite):
    def __init__(self, image, tile_x, tile_y):
        pg.sprite.Sprite.__init__(self)
        self.level = 1
        self.damage = TOWER_DATA[self.level - 1].get("damage")
        self.range = TOWER_DATA[self.level - 1].get("range")
        self.cooldown = TOWER_DATA[self.level - 1].get("cooldown")
        self.cost = TOWER_DATA[self.level - 1].get("cost")

        self.target = None
        self.selected = False
        self.last_shot = pg.time.get_ticks() - self.cooldown

        self.tile_x = tile_x
        self.tile_y = tile_y
        self.x = (self.tile_x + 0.5) * c.TILE_SIZE
        self.y = (self.tile_y + 0.5) * c.TILE_SIZE

        self.angle = 90
        self.original_image = image
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def update(self, enemy_group):
        if pg.time.get_ticks() - self.last_shot > self.cooldown and self.target:
            self.target.health -= self.damage
            self.last_shot = pg.time.get_ticks()
        self.pick_target(enemy_group)

    def upgrade(self):
        self.level += 1
        self.damage = TOWER_DATA[self.level - 1].get("damage")
        self.range = TOWER_DATA[self.level - 1].get("range")
        self.cooldown = TOWER_DATA[self.level - 1].get("cooldown")
        self.cost = TOWER_DATA[self.level - 1].get("cost")

        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range)
        self.range_image.set_alpha(100)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = self.rect.center

    def pick_target(self, enemy_group):
        for enemy in enemy_group:
            x_dist = enemy.pos[0] - self.x
            y_dist = enemy.pos[1] - self.y
            dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
            if dist < self.range:
                self.target = enemy
                self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                return

    def draw(self, surface):
        self.image = pg.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)
