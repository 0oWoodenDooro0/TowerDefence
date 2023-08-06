import math

import pygame as pg
from pygame import Vector2

from enemy import Enemy
from tower_data import TOWER_EFFECTIVENESS, TOWER_NAME


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, target: Enemy, damage: int, tower_type: int, bullet_image='assets/bullet/bullet.png'):
        pg.sprite.Sprite.__init__(self)
        self.speed = 15
        self.pos = Vector2(x, y)
        self.image = pg.image.load(bullet_image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.target = target
        self.damage = damage
        self.collided = False
        self.tower_type = tower_type

    def update(self, world, enemy_group):
        target_vector = Vector2(self.target.pos)
        movement = target_vector - self.pos
        dist = movement.length()
        if dist >= self.speed * world.game_speed:
            self.pos += movement.normalize() * self.speed * world.game_speed
        else:
            if dist != 0:
                self.pos += movement.normalize() * dist
            self.collided = True
            self.target.health -= self.damage * TOWER_EFFECTIVENESS[self.tower_type].get(self.target.enemy_type)

        if self.collided:
            self.kill()

        self.rect.center = self.pos


class DiffusionBullet(Bullet):
    def __init__(self, x, y, target: Enemy, damage: int, tower_type: int):
        Bullet.__init__(self, x, y, target, damage, tower_type, 'assets/bullet/diffusion_bullet.png')
        self.range = 42

    def update(self, world, enemy_group):
        target_vector = Vector2(self.target.pos)
        movement = target_vector - self.pos
        dist = movement.length()
        if dist >= self.speed * world.game_speed:
            self.pos += movement.normalize() * self.speed * world.game_speed
        else:
            if dist != 0:
                self.pos += movement.normalize() * dist
            self.collided = True
            for enemy in enemy_group:
                if enemy.health > 0 and self.target != enemy:
                    x_dist = enemy.pos[0] - self.pos[0]
                    y_dist = enemy.pos[1] - self.pos[1]
                    dist = math.sqrt(x_dist ** 2 + y_dist ** 2)
                    if dist < self.range:
                        enemy.health -= 0.6 * self.damage * TOWER_EFFECTIVENESS[TOWER_NAME[self.tower_type]].get(self.target.enemy_type)
            self.target.health -= self.damage * TOWER_EFFECTIVENESS[TOWER_NAME[self.tower_type]].get(self.target.enemy_type)

        if self.collided:
            self.kill()

        self.rect.center = self.pos
