import pygame as pg

import constants as c
from button import Button
from enemy import Enemy
from tower import Tower
from world import World

pg.init()

clock = pg.time.Clock()

screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption(c.TITLE)
# game variables
last_enemy_spawn = pg.time.get_ticks()
selected_tower: Tower | None = None
selected_tile: tuple | None = None

# load images
map_image = pg.image.load('assets/level/level1.png').convert_alpha()

cursor_tower = pg.image.load('assets/tower/tower1.png').convert_alpha()

enemy_images = {
    "basic": pg.image.load('assets/enemy/enemy1.png').convert_alpha(),
    "fast": pg.image.load('assets/enemy/enemy2.png').convert_alpha(),
    "strong": pg.image.load('assets/enemy/enemy3.png').convert_alpha()
}

buy_tower_image = pg.image.load('assets/buttons/buy_tower.png').convert_alpha()
upgrade_tower_image = pg.image.load('assets/buttons/upgrade_tower.png').convert_alpha()
cancel_image = pg.image.load('assets/buttons/cancel.png').convert_alpha()

# load font
text_font = pg.font.Font('assets/NotoSansTC-Regular.otf', 24)


def create_tower(selected_tile):
    new_tower = Tower(cursor_tower, selected_tile[0], selected_tile[1])
    tower_group.add(new_tower)


def select_tile(mouse_pos):
    mouse_tile_x = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_y = mouse_pos[1] // c.TILE_SIZE
    mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
    if world.tile_map[mouse_tile_num] == world.tower_tile_id:
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


def draw_text(text: str, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))


world = World(map_image)
world.process_enemies()

enemy_group = pg.sprite.Group()
tower_group = pg.sprite.Group()

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

    draw_text(f'Health: {world.health}', text_font, "black", c.SCREEN_WIDTH + 5, 0)
    draw_text(f'Money: {world.money}', text_font, "black", c.SCREEN_WIDTH + 5, 25)

    if pg.time.get_ticks() - last_enemy_spawn > c.SPAWN_COOLDOWN:
        if world.spawned_enemies < len(world.enemy_list):
            enemy_type = world.enemy_list[world.spawned_enemies]
            enemy = Enemy(enemy_type, world.waypoints, enemy_images)
            enemy_group.add(enemy)
            world.spawned_enemies += 1
            last_enemy_spawn = pg.time.get_ticks()

    if selected_tile:
        if buy_tower_button.draw(screen) and world.money > c.TOWER_COST:
            create_tower(selected_tile)
            world.money -= c.TOWER_COST
            selected_tile = None
    elif selected_tower:
        selected_tower.selected = True
        if selected_tower.level < c.MAX_LEVEL and upgrade_tower_button.draw(screen) and world.money > selected_tower.cost:
            world.money -= selected_tower.cost
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
