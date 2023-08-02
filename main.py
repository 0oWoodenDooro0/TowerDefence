import pygame as pg

import constants as c
from enemy import Enemy
from tower import Tower
from world import World
from button import Button

pg.init()

clock = pg.time.Clock()

screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption(c.TITLE)

selected_tower: Tower | None = None
selected_tile: tuple | None = None

map_image = pg.image.load('assets/level/level1.png').convert_alpha()

cursor_tower = pg.image.load('assets/tower/tower1.png').convert_alpha()

enemy_image = pg.image.load('assets/enemy/enemy1.png').convert_alpha()

buy_tower_image = pg.image.load('assets/buttons/buy_tower.png').convert_alpha()
upgrade_tower_image = pg.image.load('assets/buttons/upgrade_tower.png').convert_alpha()
cancel_image = pg.image.load('assets/buttons/cancel.png').convert_alpha()


def create_tower(selected_tile):
    new_tower = Tower(cursor_tower, selected_tile[0], selected_tile[1])
    tower_group.add(new_tower)


def select_tile(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
    if world.tile_map[mouse_tile_num] == c.TOWER_TILE_ID:
        space_is_free = True
        for tower in tower_group:
            if (mouse_tile_x, mouse_tile_y) == (tower.tile_x, tower.tile_y):
                space_is_free = False
        if space_is_free:
            return (mouse_tile_x, mouse_tile_y)
    return None


def select_tower(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    for tower in tower_group:
        if (mouse_tile_x, mouse_tile_y) == (tower.tile_x, tower.tile_y):
            return tower
    return None


def clear_selection():
    for tower in tower_group:
        tower.selected = False


world = World(map_image)

enemy_group = pg.sprite.Group()
tower_group = pg.sprite.Group()

enemy = Enemy(c.WAYPOINTS, enemy_image)

enemy_group.add(enemy)

buy_tower_button = Button(c.SCREEN_WIDTH + 20, c.SCREEN_HEIGHT - 60, buy_tower_image, True)
upgrade_tower_button = Button(c.SCREEN_WIDTH + 20, c.SCREEN_HEIGHT - 60, upgrade_tower_image, True)
# cancel_button = Button(c.SCREEN_WIDTH + c.SIDE_PANEL - 140, c.SCREEN_HEIGHT - 60, cancel_image, True)

run = True
while run:

    clock.tick(c.FPS)
    # Updating
    screen.fill("grey100")

    enemy_group.update()
    tower_group.update(enemy_group)

    if selected_tower:
        selected_tower.selected = True
    # Drawing
    world.draw(screen)

    enemy_group.draw(screen)
    for tower in tower_group:
        tower.draw(screen)

    if selected_tile:
        if buy_tower_button.draw(screen):
            create_tower(selected_tile)
            selected_tile = None
    elif selected_tower:
        selected_tower.selected = True
        if upgrade_tower_button.draw(screen):
            selected_tower.upgrade()

    # event
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                selected_tower = None
                clear_selection()
                selected_tower = select_tower(mouse_pos)
                if selected_tower is None:
                    selected_tile = select_tile(mouse_pos)

    pg.display.flip()

pg.quit()
