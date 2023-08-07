import pygame as pg

import constants as c
from button import Button
from enemy import Enemy
from enemy_data import ENEMY_SPAWN_DATA
from tower import Tower, AttackTower, EffectTower, RangeOnlyTower
from tower_data import TOWER_TYPE_DATA, TOWER_DATA, TOWER_NAME
from world import World

pg.init()

clock = pg.time.Clock()

screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
pg.display.set_caption(c.TITLE)

# load font
text_font = pg.font.Font('assets/DigitalDisco-Thin.ttf', 24)
title_font = pg.font.Font('assets/DigitalDisco-Thin.ttf', 100)


def draw_text(text: str, font, text_color, x, y, center=False):
    img = font.render(text, True, text_color)
    if center:
        img_rect = img.get_rect(center=(x, y))
        screen.blit(img, img_rect)
    else:
        screen.blit(img, (x, y))


def play_level(map_dir, tile_map, tower_tile_id, waypoints, health, money):
    # game variables
    level_started: bool = False
    selected_tower: Tower | None = None
    selected_tile: tuple | None = None
    selected_tower_type: str | None = None

    # load images
    map_image = pg.image.load(map_dir).convert_alpha()

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
    tower_btn_image = [
        pg.image.load('assets/buttons/tower1_btn.png').convert_alpha(),
        pg.image.load('assets/buttons/tower2_btn.png').convert_alpha(),
        pg.image.load('assets/buttons/tower3_btn.png').convert_alpha(),
        pg.image.load('assets/buttons/tower4_btn.png').convert_alpha()
    ]

    speed_btn_image = [
        pg.image.load('assets/buttons/speed1x.png').convert_alpha(),
        pg.image.load('assets/buttons/speed2x.png').convert_alpha(),
        pg.image.load('assets/buttons/speed3x.png').convert_alpha()
    ]
    game_pause_image = pg.image.load('assets/buttons/game_pause.png').convert_alpha()
    pause_image = pg.image.load('assets/buttons/pause.png').convert_alpha()
    resume_image = pg.image.load('assets/buttons/resume.png').convert_alpha()

    def create_tower(tile_pos, range_only=False):
        if range_only:
            new_tower = RangeOnlyTower(tower_images, tower_base_images, selected_tower_type, tile_pos)
        else:
            match selected_tower_type:
                case "basic" | "sniper" | "cannon":
                    new_tower = AttackTower(tower_images, tower_base_images, selected_tower_type, tile_pos)
                case "freeze":
                    new_tower = EffectTower(tower_images, tower_base_images, selected_tower_type, tile_pos)
                case _:
                    new_tower = None
        tower_group.add(new_tower)
        return new_tower

    def select_tile(pos):
        mouse_tile_x = pos[0] // c.TILE_SIZE
        mouse_tile_y = pos[1] // c.TILE_SIZE
        mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
        if world.tile_map[mouse_tile_num] == world.tower_tile_id:
            space_is_free = True
            for t in tower_group:
                if (mouse_tile_x, mouse_tile_y) == (t.tile_x, t.tile_y):
                    space_is_free = False
            if space_is_free:
                return mouse_tile_x, mouse_tile_y
        return None

    def select_tower(pos):
        mouse_tile_x = pos[0] // c.TILE_SIZE
        mouse_tile_y = pos[1] // c.TILE_SIZE
        for t in tower_group:
            if (mouse_tile_x, mouse_tile_y) == (t.tile_x, t.tile_y):
                return t
        return None

    def clear_selection():
        for t in tower_group:
            t.selected = False

    def clean_range_only_tower():
        for t in tower_group:
            if type(t) == RangeOnlyTower:
                t.kill()

    world = World(map_image, tile_map, tower_tile_id, waypoints, health, money, pg.time.get_ticks())
    world.process_enemies()

    enemy_group = pg.sprite.Group()
    tower_group = pg.sprite.Group()
    bullet_group = pg.sprite.Group()

    buy_tower_button = Button(c.SCREEN_WIDTH + 20, c.SCREEN_HEIGHT - 60, buy_tower_image, True, True)
    start_button = Button(c.SCREEN_WIDTH + 20, (c.SCREEN_HEIGHT - 30) // 2 + 100, start_image)
    sell_button = Button(c.SCREEN_WIDTH + c.SIDE_PANEL - 140, c.SCREEN_HEIGHT - 60, sell_image)
    game_pause_button = Button(42, 42, game_pause_image, center=True)
    tower_button = []

    for i in range(4):
        tower_button.append(Button(c.SCREEN_WIDTH + 15 + (i % 3) * 95, (c.SCREEN_HEIGHT - 30) // 2 + 190 + (i // 3) * 95, tower_btn_image[i]))
    speed_up_button = Button(c.SCREEN_WIDTH + c.SIDE_PANEL - 140, (c.SCREEN_HEIGHT - 30) // 2 + 100, speed_btn_image[0])

    run = True
    while run:

        clock.tick(c.FPS)

        # Updating
        world.update()
        if not world.game_over and not world.run_pause:
            enemy_group.update(world)
            bullet_group.update(world, enemy_group)
            tower_group.update(enemy_group, bullet_group, world)

            if selected_tower:
                selected_tower.selected = True
        # Drawing
        screen.fill("grey100")

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

        if not world.game_over:
            if game_pause_button.draw(screen):
                pass

            if speed_up_button.draw(screen):
                world.update_speed()
                world.last_enemy_spawn = (pg.time.get_ticks() - world.last_enemy_spawn) / world.game_speed + world.last_enemy_spawn
                speed_up_button.change_image(speed_btn_image[world.game_speed - 1])

            if not level_started:
                draw_text(f'regular: {ENEMY_SPAWN_DATA[world.level].get("regular")}', text_font, "black", c.SCREEN_WIDTH + 5, 350)
                draw_text(f'fast: {ENEMY_SPAWN_DATA[world.level].get("fast")}', text_font, "black", c.SCREEN_WIDTH + 5, 380)
                draw_text(f'strong: {ENEMY_SPAWN_DATA[world.level].get("strong")}', text_font, "black", c.SCREEN_WIDTH + 5, 410)
                start_button.change_image(start_image)
                if start_button.draw(screen):
                    world.level += 1
                    level_started = True
            else:
                if world.run_pause:
                    start_button.change_image(resume_image)
                else:
                    start_button.change_image(pause_image)
                if start_button.draw(screen):
                    world.pause(pg.time.get_ticks())
                    for tower in tower_group:
                        if type(tower) is AttackTower:
                            tower.pause(pg.time.get_ticks(), world)

                if pg.time.get_ticks() - world.last_enemy_spawn > c.SPAWN_COOLDOWN / world.game_speed and not world.run_pause:
                    if world.spawned_enemies < len(world.enemy_list):
                        enemy_type = world.enemy_list[world.spawned_enemies]
                        enemy = Enemy(enemy_type, world.waypoints, enemy_images, world.level)
                        enemy_group.add(enemy)
                        world.spawned_enemies += 1
                        world.last_enemy_spawn = pg.time.get_ticks()

            if world.check_level_completed():
                if world.level < len(ENEMY_SPAWN_DATA):
                    level_started = False
                    world.last_enemy_spawn = pg.time.get_ticks()
                    world.reset_level()
                    world.process_enemies()
                else:
                    world.game_over = True

            if selected_tile:
                for i in range(4):
                    if tower_button[i].draw(screen):
                        selected_tower_type = TOWER_NAME[i]
                        clean_range_only_tower()
                        selected_tower = create_tower(selected_tile, True)
                if selected_tower_type is not None:
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
                        buy_tower_button.change_image(buy_tower_image)
                        if buy_tower_button.draw(screen)[0]:
                            clean_range_only_tower()
                            selected_tower = create_tower(selected_tile)
                            world.money -= tower_cost
                            selected_tile = None
                    else:
                        buy_tower_button.change_image(buy_tower_not_enabled_image)
                        buy_tower_button.draw(screen)
            elif selected_tower:
                selected_tower.selected = True
                draw_text(f'Tower Type: {selected_tower.tower_type}', text_font, "black", c.SCREEN_WIDTH + 5, 150)
                if selected_tower.level < len(TOWER_DATA[selected_tower.tower_type]):
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
                        buy_tower_button.change_image(upgrade_tower_image)
                        buy_tower_button_clicked = buy_tower_button.draw(screen)
                        if buy_tower_button_clicked[0]:
                            world.money -= selected_tower.cost
                            selected_tower.upgrade()
                        elif buy_tower_button_clicked[1]:
                            selected_tower.check_range = True
                        else:
                            selected_tower.check_range = False
                    else:
                        buy_tower_button.change_image(upgrade_tower_not_enabled_image)
                        buy_tower_button_clicked = buy_tower_button.draw(screen)
                        if buy_tower_button_clicked[1]:
                            selected_tower.check_range = True
                        else:
                            selected_tower.check_range = False
                else:
                    match selected_tower.tower_type:
                        case "basic" | "sniper" | "cannon":
                            draw_text(f'damage: {TOWER_DATA[selected_tower.tower_type][selected_tower.level - 1].get("damage")}', text_font, "black", c.SCREEN_WIDTH + 5, 180)
                            draw_text(f'range: {TOWER_DATA[selected_tower.tower_type][selected_tower.level - 1].get("range")}', text_font, "black", c.SCREEN_WIDTH + 5, 210)
                            draw_text(f'attack speed: {1000 / TOWER_DATA[selected_tower.tower_type][selected_tower.level - 1].get("cooldown"):.2f}', text_font, "black",
                                      c.SCREEN_WIDTH + 5, 240)
                        case "freeze":
                            draw_text(f'slow_rate: {1 - TOWER_DATA[selected_tower.tower_type][selected_tower.level - 1].get("slow_rate"):.2f}', text_font, "black",
                                      c.SCREEN_WIDTH + 5,
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
                    selected_tower_type = None
                    clear_selection()
                    clean_range_only_tower()
                    selected_tower = select_tower(mouse_pos)
                    if selected_tower is None:
                        selected_tile = select_tile(mouse_pos)
                    else:
                        selected_tile = None

        pg.display.flip()


def menu():
    # load images
    select_level_image = pg.image.load('assets/buttons/select_level.png').convert_alpha()
    research_image = pg.image.load('assets/buttons/research.png').convert_alpha()
    exit_image = pg.image.load('assets/buttons/exit.png').convert_alpha()

    select_level_button = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) // 2 - 60, 700, select_level_image)
    research_button = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) // 2 - 60, 780, research_image)
    exit_button = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) // 2 - 60, 860, exit_image)

    run = True
    while run:

        clock.tick(c.FPS)

        screen.fill((0, 0, 0))

        draw_text('Tower Defense', title_font, "grey100", (c.SCREEN_WIDTH + c.SIDE_PANEL) // 2, 200, True)

        if select_level_button.draw(screen):
            select_level()
        if research_button.draw(screen):
            pass
        if exit_button.draw(screen):
            run = False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        pg.display.flip()


def select_level():
    # Load image
    level_image = pg.image.load('assets/buttons/level.png').convert_alpha()
    arrow_back_image = pg.image.load('assets/buttons/arrow_back.png').convert_alpha()

    level_button = Button(0, 0, level_image)
    arrow_back_button = Button(100, 100, arrow_back_image, center=True)

    run = True
    while run:
        clock.tick(c.FPS)

        screen.fill((0, 0, 0))

        draw_text('Level Select', title_font, "grey100", (c.SCREEN_WIDTH + c.SIDE_PANEL) // 2, 100, center=True)

        if arrow_back_button.draw(screen):
            run = False

        for i in range(20):
            x = 252 + (i % 10) * 84
            y = 252 + (i // 10) * 84
            level_button.change_pos(x, y, True)
            if level_button.draw(screen):
                play_level('assets/level/level1.png', c.TILE_MAP, c.TOWER_TILE_ID, c.WAYPOINTS, c.HEALTH, c.MONEY)
            draw_text(str(i + 1), text_font, "grey100", x, y, center=True)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        pg.display.flip()


menu()
pg.quit()
