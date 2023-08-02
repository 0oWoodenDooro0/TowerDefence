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

placing_tower = False
selected_tower = None

map_image = pg.image.load('assets/level/level1.png').convert_alpha()

cursor_tower = pg.image.load('assets/tower/tower1.png').convert_alpha()

enemy_image = pg.image.load('assets/enemy/enemy1.png').convert_alpha()

buy_tower_image = pg.image.load('assets/buttons/buy_tower.png').convert_alpha()
cancel_image = pg.image.load('assets/buttons/cancel.png').convert_alpha()


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
            new_tower = Tower(cursor_tower, mouse_tile_x, mouse_tile_y)
            tower_group.add(new_tower)


def select_tower(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    for tower in tower_group:
        if (mouse_tile_x, mouse_tile_y) == (tower.tile_x, tower.tile_y):
            return tower


def clear_selection():
    for tower in tower_group:
        tower.selected = False


world = World(map_image)

enemy_group = pg.sprite.Group()
tower_group = pg.sprite.Group()

enemy = Enemy(c.WAYPOINTS, enemy_image)

enemy_group.add(enemy)

tower_button = Button(c.SCREEN_WIDTH + 30, 120, buy_tower_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 30, 180, cancel_image, True)

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

    if tower_button.draw(screen):
        placing_tower = True
    if placing_tower:
        cursor_rect = cursor_tower.get_rect()
        cursor_pos = pg.mouse.get_pos()
        cursor_rect.center = cursor_pos
        if cursor_pos[0] <= c.SCREEN_WIDTH:
            screen.blit(cursor_tower, cursor_rect)
        if cancel_button.draw(screen):
            placing_tower = False
    # event
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                selected_tower = None
                clear_selection()
                if placing_tower:
                    create_tower(mouse_pos)
                else:
                    selected_tower = select_tower(mouse_pos)

    pg.display.flip()

pg.quit()
