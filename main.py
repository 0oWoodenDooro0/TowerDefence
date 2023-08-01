import constants as c
import pygame as pg
from enemy import Enemy
from world import World
from tower import Tower

pg.init()

clock = pg.time.Clock()

screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pg.display.set_caption(c.TITLE)

map_image = pg.image.load('assets/level/level1.png').convert_alpha()

enemy_image = pg.image.load('assets/enemy/enemy1.png').convert_alpha()

cursor_tower = pg.image.load('assets/tower/tower1.png').convert_alpha()

world = World(map_image)

enemy_group = pg.sprite.Group()
tower_group = pg.sprite.Group()

enemy = Enemy(c.WAYPOINTS, enemy_image)

enemy_group.add(enemy)

run = True
while run:

    clock.tick(c.FPS)

    screen.fill("grey100")

    world.draw(screen)

    enemy_group.update()

    enemy_group.draw(screen)
    tower_group.draw(screen)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            tower = Tower(cursor_tower, mouse_pos)
            tower_group.add(tower)

    pg.display.flip()

pg.quit()
