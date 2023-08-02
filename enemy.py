import math

import pygame as pg
from pygame.math import Vector2

from enemy_data import ENEMY_DATA


class Enemy(pg.sprite.Sprite):
    def __init__(self, enemy_type: str, waypoints: list, images: dict):
        pg.sprite.Sprite.__init__(self)
        self.health = ENEMY_DATA.get(enemy_type)["health"]
        self.speed = ENEMY_DATA.get(enemy_type)["speed"]
        self.money = ENEMY_DATA.get(enemy_type)["money"]

        self.target = None
        self.movement = None
        self.waypoints = waypoints
        self.target_waypoint = 1
        self.pos = Vector2(self.waypoints[0])
        self.angle = 0
        self.original_image = images.get(enemy_type)
        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, world):
        self.check_alive(world)
        self.move(world)
        self.rotate()

    def move(self, world):
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            world.health -= 1
            world.missed_enemies += 1
            self.kill()

        dist = self.movement.length()

        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1

        self.rect.center = self.pos

    def rotate(self):
        dist = self.target - self.pos

        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))

        self.image = pg.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def check_alive(self, world):
        if self.health <= 0:
            world.money += self.money
            world.killed_enemies += 1
            self.kill()
