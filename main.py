import pygame as pg

import constants as c
from button import Button
from enemy import Enemy
from tower import Tower, AttackTower, EffectTower
from tower_data import TOWER_TYPE_DATA, TOWER_DATA
from world import World
from enemy_data import ENEMY_SPAWN_DATA

pg.init()

clock = pg.time.Clock()

screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption(c.TITLE)
# game variables
level_started: bool = False
game_over: bool = False
last_enemy_spawn = pg.time.get_ticks()
selected_tower: Tower | None = None
selected_tile: tuple | None = None
selected_tower_type: str | None = None

# load images
map_image = pg.image.load('assets/level/level1.png').convert_alpha()

tower_images = {
    "basic": pg.image.load('assets/tower/tower1.png').convert_alpha(),
    "sniper": pg.image.load('assets/tower/tower2.png').convert_alpha(),
    "cannon": pg.image.load('assets/tower/tower3.png').convert_alpha(),
    "freeze": pg.image.load('assets/tower/tower4.png').convert_alpha()
}

tower_base_images = {
    "basic": pg.image.load('assets/tower/tower_base1.png').convert_alpha(),
    "sniper": pg.image.load('assets/tower/tower_base2.png').convert_alpha(),
    "cannon": pg.image.load('assets/tower/tower_base3.png').convert_alpha(),
    "freeze": pg.image.load('assets/tower/tower_base4.png').convert_alpha()
}

enemy_images = {
    "regular": pg.image.load('assets/enemy/enemy1.png').convert_alpha(),
    "fast": pg.image.load('assets/enemy/enemy2.png').convert_alpha(),
    "strong": pg.image.load('assets/enemy/enemy3.png').convert_alpha()
}

buy_tower_image = pg.image.load('assets/buttons/buy_tower.png').convert_alpha()
buy_tower_not_enabled_image = pg.image.load('assets/buttons/buy_tower_not_enabled.png').convert_alpha()
upgrade_tower_image = pg.image.load('assets/buttons/upgrade_tower.png').convert_alpha()
upgrade_tower_not_enabled_image = pg.image.load('assets/buttons/upgrade_tower_not_enabled.png')
start_image = pg.image.load('assets/buttons/start.png').convert_alpha()
sell_image = pg.image.load('assets/buttons/sell.png').convert_alpha()
tower1_btn_image = pg.image.load('assets/buttons/tower1_btn.png').convert_alpha()
tower2_btn_image = pg.image.load('assets/buttons/tower2_btn.png').convert_alpha()
tower3_btn_image = pg.image.load('assets/buttons/tower3_btn.png').convert_alpha()
tower4_btn_image = pg.image.load('assets/buttons/tower4_btn.png').convert_alpha()

speed_btn_image = [
    pg.image.load('assets/buttons/speed1x.png').convert_alpha(),
    pg.image.load('assets/buttons/speed2x.png').convert_alpha(),
    pg.image.load('assets/buttons/speed3x.png').convert_alpha()
]

bullet_image = pg.image.load('assets/bullet/bullet.png').convert_alpha()

# load font
text_font = pg.font.Font('assets/NotoSansTC-Regular.otf', 24)


def create_tower(selected_tile):
    match selected_tower_type:
        case "basic" | "sniper" | "cannon":
            new_tower = AttackTower(tower_images, tower_base_images, selected_tower_type, selected_tile)
        case "freeze":
            new_tower = EffectTower(tower_images, tower_base_images, selected_tower_type, selected_tile)
    tower_group.add(new_tower)
    return new_tower


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
bullet_group = pg.sprite.Group()

buy_tower_button = Button(c.SCREEN_WIDTH + 20, c.SCREEN_HEIGHT - 60, buy_tower_image, True, False)
start_button = Button(c.SCREEN_WIDTH + 20, (c.SCREEN_HEIGHT - 30) // 2 + 100, start_image, True, False)
sell_button = Button(c.SCREEN_WIDTH + c.SIDE_PANEL - 140, c.SCREEN_HEIGHT - 60, sell_image, True, False)
tower1_button = Button(c.SCREEN_WIDTH + 15, (c.SCREEN_HEIGHT - 30) // 2 + 190, tower1_btn_image, True, False)
tower2_button = Button(c.SCREEN_WIDTH + 110, (c.SCREEN_HEIGHT - 30) // 2 + 190, tower2_btn_image, True, False)
tower3_button = Button(c.SCREEN_WIDTH + 205, (c.SCREEN_HEIGHT - 30) // 2 + 190, tower3_btn_image, True, False)
tower4_button = Button(c.SCREEN_WIDTH + 15, (c.SCREEN_HEIGHT - 30) // 2 + 285, tower4_btn_image, True, False)
speed_up_button = Button(c.SCREEN_WIDTH + c.SIDE_PANEL - 140, (c.SCREEN_HEIGHT - 30) // 2 + 100, speed_btn_image[0], True, False)

run = True
while run:

    clock.tick(c.FPS)

    # Updating
    screen.fill("grey100")
    if not game_over:
        if world.health <= 0:
            game_over = True

        enemy_group.update(world)
        bullet_group.update(world, enemy_group)
        tower_group.update(enemy_group, bullet_group, world)

        if selected_tower:
            selected_tower.selected = True
    # Drawing
    world.draw(screen)

    enemy_group.draw(screen)
    for enemy in enemy_group:
        enemy.health_bar.draw(screen)
    for tower in tower_group:
        tower.draw(screen)
    bullet_group.draw(screen)

    draw_text(f'Health: {world.health}', text_font, "black", c.SCREEN_WIDTH + 5, 0)
    draw_text(f'Money: {world.money}', text_font, "black", c.SCREEN_WIDTH + 5, 30)
    draw_text(f'Level: {world.level}', text_font, "black", c.SCREEN_WIDTH + 5, 60)

    if not game_over:

        if speed_up_button.draw(screen):
            world.update_speed()
            last_enemy_spawn = (pg.time.get_ticks() - last_enemy_spawn) / world.game_speed + last_enemy_spawn
            speed_up_button.change_image(c.SCREEN_WIDTH + c.SIDE_PANEL - 140, (c.SCREEN_HEIGHT - 30) // 2 + 100, speed_btn_image[world.game_speed - 1])

        if not level_started:
            draw_text(f'regular: {ENEMY_SPAWN_DATA[world.level].get("regular")}', text_font, "black", c.SCREEN_WIDTH + 5, 350)
            draw_text(f'fast: {ENEMY_SPAWN_DATA[world.level].get("fast")}', text_font, "black", c.SCREEN_WIDTH + 5, 380)
            draw_text(f'strong: {ENEMY_SPAWN_DATA[world.level].get("strong")}', text_font, "black", c.SCREEN_WIDTH + 5, 410)
            if start_button.draw(screen):
                world.level += 1
                level_started = True
        else:
            if pg.time.get_ticks() - last_enemy_spawn > c.SPAWN_COOLDOWN / world.game_speed:
                if world.spawned_enemies < len(world.enemy_list):
                    enemy_type = world.enemy_list[world.spawned_enemies]
                    enemy = Enemy(enemy_type, world.waypoints, enemy_images, world.level)
                    enemy_group.add(enemy)
                    world.spawned_enemies += 1
                    last_enemy_spawn = pg.time.get_ticks()

        if world.check_level_completed():
            if world.level < c.MAP_MAX_LEVEL:
                level_started = False
                last_enemy_spawn = pg.time.get_ticks()
                world.reset_level()
                world.process_enemies()
            else:
                game_over = True

        if selected_tile:
            if tower1_button.draw(screen):
                selected_tower_type = "basic"
            if tower2_button.draw(screen):
                selected_tower_type = "sniper"
            if tower3_button.draw(screen):
                selected_tower_type = "cannon"
            if tower4_button.draw(screen):
                selected_tower_type = "freeze"
            if selected_tower_type:
                draw_text(f'Tower Type: {selected_tower_type}', text_font, "black", c.SCREEN_WIDTH + 5, 150)
                match selected_tower_type:
                    case "basic" | "sniper" | "cannon":
                        draw_text(f'damage: {TOWER_DATA[selected_tower_type][0].get("damage")}', text_font, "black", c.SCREEN_WIDTH + 5, 180)
                        draw_text(f'attack speed: {1000 / TOWER_DATA[selected_tower_type][0].get("cooldown"):.2f}', text_font, "black", c.SCREEN_WIDTH + 5, 210)
                        draw_text(f'range: {TOWER_DATA[selected_tower_type][0].get("range")}', text_font, "black", c.SCREEN_WIDTH + 5, 240)
                    case "freeze":
                        draw_text(f'slow_rate: {1 - TOWER_DATA[selected_tower_type][0].get("slow_rate"):.2f}', text_font, "black", c.SCREEN_WIDTH + 5, 180)
                        draw_text(f'range: {TOWER_DATA[selected_tower_type][0].get("range")}', text_font, "black", c.SCREEN_WIDTH + 5, 210)
                tower_cost = TOWER_TYPE_DATA[selected_tower_type].get("cost")
                draw_text(f'Cost: {tower_cost}', text_font, "black", c.SCREEN_WIDTH + 30, c.SCREEN_HEIGHT - 110)
                if world.money >= tower_cost:
                    buy_tower_button.change_image(c.SCREEN_WIDTH + 20, c.SCREEN_HEIGHT - 60, buy_tower_image)
                    if buy_tower_button.draw(screen):
                        selected_tower = create_tower(selected_tile)
                        world.money -= tower_cost
                        selected_tile = None
                else:
                    buy_tower_button.change_image(c.SCREEN_WIDTH + 20, c.SCREEN_HEIGHT - 60, buy_tower_not_enabled_image)
                    buy_tower_button.draw(screen)
        elif selected_tower:
            selected_tower.selected = True
            draw_text(f'Tower Type: {selected_tower.tower_type}', text_font, "black", c.SCREEN_WIDTH + 5, 150)
            if selected_tower.level < c.TOWER_MAX_LEVEL:
                draw_text(f'Cost: {selected_tower.cost}', text_font, "black", c.SCREEN_WIDTH + 30, c.SCREEN_HEIGHT - 110)
                match selected_tower.tower_type:
                    case "basic" | "sniper" | "cannon":
                        draw_text(
                            f'damage: {TOWER_DATA[selected_tower.tower_type][selected_tower.level - 1].get("damage")} -> {TOWER_DATA[selected_tower.tower_type][selected_tower.level].get("damage")}',
                            text_font, "black", c.SCREEN_WIDTH + 5, 180)
                        draw_text(
                            f'range: {TOWER_DATA[selected_tower.tower_type][selected_tower.level - 1].get("range")} -> {TOWER_DATA[selected_tower.tower_type][selected_tower.level].get("range")}',
                            text_font, "black", c.SCREEN_WIDTH + 5, 210)
                        draw_text(
                            f'attack speed: {1000 / TOWER_DATA[selected_tower.tower_type][selected_tower.level - 1].get("cooldown"):.2f} -> {1000 / TOWER_DATA[selected_tower.tower_type][selected_tower.level].get("cooldown"):.2f}',
                            text_font, "black", c.SCREEN_WIDTH + 5, 240)
                    case "freeze":
                        draw_text(
                            f'slow_rate: {1 - TOWER_DATA[selected_tower.tower_type][selected_tower.level - 1].get("slow_rate"):.2f} -> {1 - TOWER_DATA[selected_tower.tower_type][selected_tower.level].get("slow_rate"):.2f}',
                            text_font, "black", c.SCREEN_WIDTH + 5, 180)
                        draw_text(
                            f'range: {TOWER_DATA[selected_tower.tower_type][selected_tower.level - 1].get("range")} -> {TOWER_DATA[selected_tower.tower_type][selected_tower.level].get("range")}',
                            text_font, "black", c.SCREEN_WIDTH + 5, 210)
                if world.money >= selected_tower.cost:
                    buy_tower_button.change_image(c.SCREEN_WIDTH + 20, c.SCREEN_HEIGHT - 60, upgrade_tower_image)
                    if buy_tower_button.draw(screen):
                        world.money -= selected_tower.cost
                        selected_tower.upgrade()
                else:
                    buy_tower_button.change_image(c.SCREEN_WIDTH + 20, c.SCREEN_HEIGHT - 60, upgrade_tower_not_enabled_image)
                    buy_tower_button.draw(screen)
            else:
                match selected_tower.tower_type:
                    case "basic" | "sniper" | "cannon":
                        draw_text(f'damage: {TOWER_DATA[selected_tower.tower_type][selected_tower.level - 1].get("damage")}', text_font, "black", c.SCREEN_WIDTH + 5, 180)
                        draw_text(f'range: {TOWER_DATA[selected_tower.tower_type][selected_tower.level - 1].get("range")}', text_font, "black", c.SCREEN_WIDTH + 5, 210)
                        draw_text(f'attack speed: {1000 / TOWER_DATA[selected_tower.tower_type][selected_tower.level - 1].get("cooldown"):.2f}', text_font, "black",
                                  c.SCREEN_WIDTH + 5, 240)
                    case "freeze":
                        draw_text(f'slow_rate: {1 - TOWER_DATA[selected_tower.tower_type][selected_tower.level - 1].get("slow_rate"):.2f}', text_font, "black", c.SCREEN_WIDTH + 5,
                                  180)
                        draw_text(f'range: {TOWER_DATA[selected_tower.tower_type][selected_tower.level - 1].get("range")}', text_font, "black", c.SCREEN_WIDTH + 5, 210)
            draw_text(f'SELL: {selected_tower.sell}', text_font, "black", c.SCREEN_WIDTH + 170, c.SCREEN_HEIGHT - 110)
            if sell_button.draw(screen):
                world.money += selected_tower.sell
                tower_group.remove(selected_tower)
                selected_tower = None

    # event
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                selected_tile = None
                selected_tower = None
                selected_tower_type = None
                clear_selection()
                selected_tower = select_tower(mouse_pos)
                if selected_tower is None:
                    selected_tile = select_tile(mouse_pos)

    pg.display.flip()

pg.quit()
