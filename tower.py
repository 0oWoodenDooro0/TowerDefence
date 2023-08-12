import math

import pygame as pg

import constants as c
from bullet import Bullet, DiffusionBullet
from tower_data import TOWER_DATA
from world import World


class Tower(pg.sprite.Sprite):
    def __init__(self, tower_images: dict, tower_base_images: dict, tower_type: str, tile_pos, bonus):
        pg.sprite.Sprite.__init__(self)
        self.level = 1
        self.tower_type = tower_type
        self.bonus = bonus
        self.range = round(self.get_attribute(0, "range"), 2) * c.TILE_SIZE
        self.cost = round(self.get_attribute(0, "cost"))
        self.sell = round(self.get_attribute(0, "sell"))

        self.target = None
        self.selected = False
        self.check_range = True

        self.tile_x = tile_pos[0]
        self.tile_y = tile_pos[1]
        self.x = (self.tile_x + 0.5) * c.TILE_SIZE
        self.y = (self.tile_y + 0.5) * c.TILE_SIZE

        self.original_image = tower_images[self.tower_type]
        self.tower_base_image = tower_base_images[self.tower_type]

        self.range_image = pg.Surface((self.range * 2, self.range * 2))
        self.range_image.fill((0, 0, 0))
        self.range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.range_image, "grey100", (self.range, self.range), self.range, width=2)
        self.range_rect = self.range_image.get_rect()
        self.range_rect.center = (self.x, self.y)

    def upgrade(self):
        self.level += 1
        self.range = round(self.get_attribute(self.level - 1, "range"), 2) * c.TILE_SIZE
        self.cost = round(self.get_attribute(self.level - 1, "cost"))
        self.sell = round(self.get_attribute(self.level - 1, "sell"))

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

    def draw_next_range(self, surface):
        if self.level >= len(TOWER_DATA[self.tower_type]):
            return None, None
        next_range = round(self.get_attribute(0, "range"), 2) * c.TILE_SIZE
        range_image = pg.Surface((next_range * 2, next_range * 2))
        range_image.fill((0, 0, 0))
        range_image.set_colorkey((0, 0, 0))
        pg.draw.circle(range_image, "grey100", (next_range, next_range), next_range, width=3)
        range_rect = range_image.get_rect()
        range_rect.center = (self.x, self.y)
        if range_image and range_rect:
            surface.blit(range_image, range_rect)

    def get_attribute(self, level: int, attribute: str, bonus: bool = True):
        return TOWER_DATA[self.tower_type][level].get(attribute) * self.bonus.get_bonus_data(attribute) if bonus else TOWER_DATA[self.tower_type][level].get(attribute)


class AttackTower(Tower):
    def __init__(self, tower_images: dict, tower_base_images: dict, tower_type: str, tile_pos, bonus):
        Tower.__init__(self, tower_images, tower_base_images, tower_type, tile_pos, bonus)
        self.damage = round(self.get_attribute(self.level - 1, "damage"), 2)
        self.atk_speed = round(self.get_attribute(self.level - 1, "atk_speed"), 2)
        self.rotate_speed = round(self.get_attribute(self.level - 1, "rotate_speed"), 2)
        self.cooldown = int(1000 / self.atk_speed)

        self.last_shot = pg.time.get_ticks() - self.cooldown
        self.elapsed_time = 0

        self.angle = 90
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def upgrade(self):
        Tower.upgrade(self)
        self.damage = round(self.get_attribute(self.level - 1, "damage"), 2)
        self.atk_speed = round(self.get_attribute(self.level - 1, "atk_speed"), 2)
        self.rotate_speed = round(self.get_attribute(self.level - 1, "rotate_speed"), 2)
        self.cooldown = int(1000 / self.atk_speed)

    def update(self, enemy_group: pg.sprite.Group, bullet_group: pg.sprite.Group, world: World):
        shoot = self.pick_target(enemy_group, world)
        if pg.time.get_ticks() - self.last_shot > self.cooldown / world.game_speed and self.target and shoot:
            match self.tower_type:
                case "basic" | "sniper":
                    new_bullet = Bullet(self.x, self.y, self.target, self.damage, self.tower_type)
                case "cannon":
                    new_bullet = DiffusionBullet(self.x, self.y, self.target, self.damage, self.tower_type)
                case _:
                    new_bullet = None
            bullet_group.add(new_bullet)
            self.last_shot = pg.time.get_ticks()
        self.target = None

    def pick_target(self, enemy_group: pg.sprite.Group, world: World):
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    self.target = enemy
                    angle = math.degrees(math.atan2(-y_dist, x_dist))
                    diff = self.angle - angle
                    if diff < -180:
                        diff += 360
                    elif diff > 180:
                        diff -= 360
                    degree = self.rotate_speed * world.game_speed / c.FPS
                    if abs(diff) > degree:
                        if diff > 0:
                            self.angle -= degree
                        else:
                            self.angle += degree
                        if self.angle > 180:
                            self.angle -= 360
                        elif self.angle < -180:
                            self.angle += 360
                    else:
                        self.angle = angle
                        return True
                    return False

    def pause(self, time, world):
        if world.run_pause:
            self.elapsed_time = time - self.last_shot
        else:
            if world.game_pause:
                self.elapsed_time = time - self.last_shot
            else:
                self.last_shot = time - self.elapsed_time

    def draw(self, surface):
        Tower.draw(self, surface)
        self.image = pg.transform.rotate(self.original_image, self.angle - 90)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        surface.blit(self.image, self.rect)
        if self.selected:
            surface.blit(self.range_image, self.range_rect)
            if self.check_range:
                Tower.draw_next_range(self, surface)


class EffectTower(Tower):
    def __init__(self, tower_images: dict, tower_base_images: dict, tower_type: str, tile_pos, bonus):
        Tower.__init__(self, tower_images, tower_base_images, tower_type, tile_pos, bonus)
        self.slow_rate = self.get_attribute(0, "slow_rate", False)

        self.rect = self.original_image.get_rect()
        self.rect.center = (self.x, self.y)

        pg.draw.circle(self.range_image, (102, 179, 255), (self.range, self.range), self.range)
        self.range_image.set_alpha(100)

    def upgrade(self):
        Tower.upgrade(self)
        self.slow_rate = self.get_attribute(self.level - 1, "slow_rate", False)
        pg.draw.circle(self.range_image, (102, 179, 255), (self.range, self.range), self.range)
        self.range_image.set_alpha(100)

    def update(self, enemy_group, bullet_group: pg.sprite.Group, world):
        for enemy in enemy_group:
            if enemy.health > 0:
                x_dist = enemy.pos[0] - self.x
                y_dist = enemy.pos[1] - self.y
                dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                if dist < self.range:
                    enemy.slow_rate = 1 - self.slow_rate
                else:
                    enemy.slow_rate = 1

    def draw(self, surface):
        Tower.draw(self, surface)
        surface.blit(self.original_image, self.rect)
        surface.blit(self.range_image, self.range_rect)
        if self.check_range and self.selected:
            Tower.draw_next_range(self, surface)


class RangeOnlyTower(Tower):
    def __init__(self, tower_images: dict, tower_base_images: dict, tower_type: str, tile_pos, bonus):
        Tower.__init__(self, tower_images, tower_base_images, tower_type, tile_pos, bonus)
        self.level = 0

    def draw(self, surface):
        if self.check_range:
            Tower.draw_next_range(self, surface)
