import pygame as pg
from pygame import Vector2
from enemy import Enemy


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, target: Enemy, damage: int):
        pg.sprite.Sprite.__init__(self)
        self.speed = 15
        self.pos = Vector2(x, y)
        self.image = pg.image.load('assets/bullet/bullet.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.target = target
        self.damage = damage
        self.collided = False

    def update(self, world):
        target_vector = Vector2(self.target.pos)
        movement = target_vector - self.pos
        dist = movement.length()
        if dist >= self.speed * world.game_speed:
            self.pos += movement.normalize() * self.speed * world.game_speed
        else:
            if dist != 0:
                self.pos += movement.normalize() * dist
            self.collided = True
            self.target.health -= self.damage

        if self.collided:
            self.kill()

        self.rect.center = self.pos
