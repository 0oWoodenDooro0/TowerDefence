import pygame as pg

import constants as c
from enemy import Enemy
from tower import Tower
from world import World

pg.init()

clock = pg.time.Clock()

screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pg.display.set_caption(c.TITLE)

map_image = pg.image.load('assets/level/level1.png').convert_alpha()

enemy_image = pg.image.load('assets/enemy/enemy1.png').convert_alpha()

cursor_tower = pg.image.load('assets/tower/tower1.png').convert_alpha()


def create_tower(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
    if world.tile_map[mouse_tile_num] == 25:
        space_is_free = True
        for tower in tower_group:
            if (mouse_tile_x, mouse_tile_y) == (tower.tile_x, tower.tile_y):
                space_is_free = False
        if space_is_free:
            tower = Tower(cursor_tower, mouse_tile_x, mouse_tile_y)
            tower_group.add(tower)


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
            create_tower(mouse_pos)

    pg.display.flip()

pg.quit()
