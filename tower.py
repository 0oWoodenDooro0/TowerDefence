import math

import pygame as pg

import constants as c
from bullet import Bullet, DiffusionBullet
from tower_data import TOWER_DATA, TOWER_NAME


class Tower(pg.sprite.Sprite):
    def __init__(self, tower_images: dict, tower_base_images: dict, tower_type: int, tile_pos):
        pg.sprite.Sprite.__init__(self)
        self.level = 1
        self.tower_type = tower_type
        self.tower_type_name = TOWER_NAME[self.tower_type]
        self.range = TOWER_DATA[self.tower_type_name][self.level - 1].get("range")
        self.cost = TOWER_DATA[self.tower_type_name][self.level - 1].get("cost")
        self.sell = TOWER_DATA[self.tower_type_name][self.level - 1].get("sell")

        self.target = None
        self.selected = False
        self.check_range = True

        self.tile_x = tile_pos[0]
        self.tile_y = tile_pos[1]
        self.x = (self.tile_x + 0.5) * c.TILE_SIZE
        self.y = (self.tile_y + 0.5) * c.TILE_SIZE

        self.original_image = tower_images[self.tower_type_name]
        self.tower_base_image = tower_base_images[self.tower_type_name]

        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range, width=2)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = (self.x, self.y)

    def upgrade(self):
        self.level += 1
        self.range = TOWER_DATA[self.tower_type_name][self.level - 1].get("range")
        self.cost = TOWER_DATA[self.tower_type_name][self.level - 1].get("cost")
        self.sell = TOWER_DATA[self.tower_type_name][self.level - 1].get("sell")

        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range, width=2)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = (self.x, self.y)

    def draw(self, surface):
        tower_base_rect = self.tower_base_image.get_rect()
        tower_base_rect.center = (self.x, self.y)
        surface.blit(self.tower_base_image, tower_base_rect)

    def draw_next_range(self):
        if self.level >= c.TOWER_MAX_LEVEL: return None, None
        range = TOWER_DATA[self.tower_type_name][self.level].get("range")
        range_image = pg.Surface((range * 2, range * 2))
        range_image.fill((0, 0, 0))
        range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(range_image, "grey100", (range, range), range, width=3)
        range_rect = range_image.get_rect()
        range_rect.center = (self.x, self.y)
        return range_image, range_rect


class AttackTower(Tower):
    def __init__(self, tower_images: dict, tower_base_images: dict, tower_type: int, tile_pos):
        Tower.__init__(self, tower_images, tower_base_images, tower_type, tile_pos)
        self.damage = TOWER_DATA[self.tower_type_name][self.level - 1].get("damage")
        self.cooldown = TOWER_DATA[self.tower_type_name][self.level - 1].get("cooldown")

        self.last_shot = pg.time.get_ticks() - self.cooldown

        self.angle = 90
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def upgrade(self):
        Tower.upgrade(self)
        self.damage = TOWER_DATA[self.tower_type_name][self.level - 1].get("damage")
        self.cooldown = TOWER_DATA[self.tower_type_name][self.level - 1].get("cooldown")

    def update(self, enemy_group, bullet_group: pg.sprite.Group, world):
        self.pick_target(enemy_group)
        if pg.time.get_ticks() - self.last_shot > self.cooldown / world.game_speed and self.target:
            match self.tower_type_name:
                case "basic" | "sniper":
                    new_bullet = Bullet(self.x, self.y, self.target, self.damage, self.tower_type_name)
                case "cannon":
                    new_bullet = DiffusionBullet(self.x, self.y, self.target, self.damage, self.tower_type_name)
            bullet_group.add(new_bullet)
            self.last_shot = pg.time.get_ticks()
        self.target = None

    def pick_target(self, enemy_group):
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    self.target = enemy
                    self.angle = math.degrees(math.atan2(-y_dist, x_dist))
                    break

    def draw(self, surface):
        Tower.draw(self, surface)
        self.image = pg.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)
            if self.check_range:
                range_image, range_rect = Tower.draw_next_range(self)
                if range_image and range_rect:
                    surface.blit(range_image, range_rect)


class EffectTower(Tower):
    def __init__(self, tower_images: dict, tower_base_images: dict, tower_type: int, tile_pos):
        Tower.__init__(self, tower_images, tower_base_images, tower_type, tile_pos)
        self.rate = TOWER_DATA[self.tower_type][self.level - 1].get("slow_rate")

        self.rect = self.original_image.get_rect()
        self.rect.center = (self.x, self.y)

        pg.draw.circle(self.range_image, (102, 179, 255), (self.range, self.range), self.range)
        self.range_image.set_alpha(100)

    def upgrade(self):
        Tower.upgrade(self)
        self.rate = TOWER_DATA[self.tower_type][self.level - 1].get("slow_rate")
        pg.draw.circle(self.range_image, (102, 179, 255), (self.range, self.range), self.range)
        self.range_image.set_alpha(100)

    def update(self, enemy_group, bullet_group: pg.sprite.Group, world):
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    enemy.slow_rate = 1 - self.rate
                else:
                    enemy.slow_rate = 1

    def draw(self, surface):
        Tower.draw(self, surface)
        surface.blit(self.original_image, self.rect)
        surface.blit(self.range_image, self.range_rect)
        if self.check_range and self.selected:
            range_image, range_rect = Tower.draw_next_range(self)
            surface.blit(range_image, range_rect)


class RangeOnlyTower(Tower):
    def __init__(self, tower_images: dict, tower_base_images: dict, tower_type: int, tile_pos):
        Tower.__init__(self, tower_images, tower_base_images, tower_type, tile_pos)
        self.level = 0

    def draw(self, surface):
        if self.check_range:
            range_image, range_rect = Tower.draw_next_range(self)
            surface.blit(range_image, range_rect)
