import json
import os

import pygame as pg

import constants as c
from button import Button
from enemy import Enemy
from enemy_data import ENEMY_SPAWN_TYPE_DATA
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


def play_level(map_dir, level_data, health, money):
    # game variables
    wave_started: bool = False
    selected_tower: Tower | None = None
    selected_tile: tuple | None = None
    selected_tower_type: str | None = None
    selected_tower_pos: tuple | None = None

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
    pause_image = pg.image.load('assets/buttons/pause.png').convert_alpha()
    resume_image = pg.image.load('assets/buttons/resume.png').convert_alpha()
    game_pause_image = pg.image.load('assets/buttons/game_pause.png').convert_alpha()
    game_resume_image = pg.image.load('assets/buttons/game_resume.png').convert_alpha()
    game_restart_image = pg.image.load('assets/buttons/game_restart.png').convert_alpha()
    game_end_image = pg.image.load('assets/buttons/game_end.png').convert_alpha()
    selected_tower_image = pg.image.load('assets/buttons/selected_tower.png').convert_alpha()
    selected_tile_image = pg.image.load('assets/buttons/selected_tile.png').convert_alpha()
    selected_tower_rect = selected_tower_image.get_rect()
    selected_tile_rect = selected_tile_image.get_rect()

    pause_mask = pg.Surface((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
    pause_mask.fill((0, 0, 0))
    pause_mask.set_alpha(100)
    pause_mask_rect = pause_mask.get_rect()
    pause_mask_rect.topleft = (0, 0)

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
        return new_tower, tile_pos

    def select_tile(pos):
        mouse_tile_x = pos[0] // c.TILE_SIZE
        mouse_tile_y = pos[1] // c.TILE_SIZE
        mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
        for tower_id in world.tower_tile_id:
            if world.tile_map[mouse_tile_num] == tower_id:
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
                return t, (mouse_tile_x, mouse_tile_y)
        return None, None

    def clear_selection():
        for t in tower_group:
            t.selected = False

    def clean_range_only_tower():
        for t in tower_group:
            if type(t) == RangeOnlyTower:
                t.kill()

    def game_pause():
        world.pause(pg.time.get_ticks())
        for t in tower_group:
            if type(t) is AttackTower:
                t.pause(pg.time.get_ticks(), world)

    world = World(map_image, level_data, health, money, pg.time.get_ticks())

    enemy_group = pg.sprite.Group()
    tower_group = pg.sprite.Group()
    bullet_group = pg.sprite.Group()

    buy_tower_button = Button(c.SCREEN_WIDTH + 20, c.SCREEN_HEIGHT - 60, buy_tower_image, True, True)
    start_button = Button(c.SCREEN_WIDTH + 20, (c.SCREEN_HEIGHT - 30) // 2 + 100, start_image)
    sell_button = Button(c.SCREEN_WIDTH + c.SIDE_PANEL - 140, c.SCREEN_HEIGHT - 60, sell_image)
    game_pause_button = Button(42, 42, game_pause_image, center=True)
    game_resume_button = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) // 2 - 60, 700, game_resume_image)
    game_restart_button = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) // 2 - 60, 780, game_restart_image)
    game_end_button = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) // 2 - 60, 860, game_end_image)

    tower_button = []

    for i in range(4):
        tower_button.append(Button(c.SCREEN_WIDTH + 15 + (i % 3) * 95, (c.SCREEN_HEIGHT - 30) // 2 + 190 + (i // 3) * 95, tower_btn_image[i]))
    speed_up_button = Button(c.SCREEN_WIDTH + c.SIDE_PANEL - 140, (c.SCREEN_HEIGHT - 30) // 2 + 100, speed_btn_image[0])

    run = True
    while run:

        clock.tick(c.FPS)

        # Updating
        world.update()
        if not world.game_over and not world.run_pause and not world.game_pause:
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
        draw_text(f'Wave: {world.wave}', text_font, "black", c.SCREEN_WIDTH + 5, 60)

        if game_pause_button.draw(screen) and not world.game_pause:
            world.game_pause = not world.game_pause
            game_pause()

        if not world.game_over:

            if speed_up_button.draw(screen) and not world.game_pause:
                world.update_speed()
                world.last_enemy_spawn = (pg.time.get_ticks() - world.last_enemy_spawn) / world.game_speed + world.last_enemy_spawn
                speed_up_button.change_image(speed_btn_image[world.game_speed - 1])

            if not wave_started:
                draw_text(f'Enemy Type: {world.next_wave_enemies_type}', text_font, "black", c.SCREEN_WIDTH + 5, 350)
                draw_text(f'Num of Enemy : {world.next_wave_enemies_num}', text_font, "black", c.SCREEN_WIDTH + 5, 380)
                start_button.change_image(start_image)
                if start_button.draw(screen):
                    world.wave += 1
                    wave_started = True
            else:
                if world.run_pause:
                    start_button.change_image(resume_image)
                else:
                    start_button.change_image(pause_image)
                if start_button.draw(screen) and not world.game_pause:
                    world.run_pause = not world.run_pause
                    game_pause()

                if pg.time.get_ticks() - world.last_enemy_spawn > world.spawn_cooldown / world.game_speed and not world.run_pause and not world.game_pause:
                    if world.spawned_enemies < len(world.enemy_list):
                        enemy_type = world.enemy_list[world.spawned_enemies]
                        enemy = Enemy(enemy_type, world.waypoints, enemy_images, world.wave)
                        enemy_group.add(enemy)
                        world.spawned_enemies += 1
                        world.last_enemy_spawn = pg.time.get_ticks()

            if world.check_wave_completed():
                wave_started = False
                world.last_enemy_spawn = pg.time.get_ticks()
                world.reset_wave()
                world.process_enemies()

            if selected_tile:
                for i in range(4):
                    if tower_button[i].draw(screen):
                        selected_tower_type = TOWER_NAME[i]
                        clean_range_only_tower()
                        selected_tower, _ = create_tower(selected_tile, True)
                        selected_tower_pos = (c.SCREEN_WIDTH + (i % 3) * 95 + 55, (c.SCREEN_HEIGHT - 30) // 2 + (i // 3) * 95 + 230)
                selected_tile_rect.center = ((selected_tile[0] + 0.5) * c.TILE_SIZE, (selected_tile[1] + 0.5) * c.TILE_SIZE)
                screen.blit(selected_tile_image, selected_tile_rect)
                if selected_tower_type is not None:
                    selected_tower_rect.center = selected_tower_pos
                    screen.blit(selected_tower_image, selected_tower_rect)
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
                            selected_tower, selected_tower_pos = create_tower(selected_tile)
                            world.money -= tower_cost
                            selected_tile = None
                    else:
                        buy_tower_button.change_image(buy_tower_not_enabled_image)
                        buy_tower_button.draw(screen)
            elif selected_tower:
                selected_tower.selected = True
                selected_tile_rect.center = ((selected_tower_pos[0] + 0.5) * c.TILE_SIZE, (selected_tower_pos[1] + 0.5) * c.TILE_SIZE)
                screen.blit(selected_tile_image, selected_tile_rect)
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
        else:
            selected_tower = None
            selected_tile = None
            selected_tower_type = None
            selected_tower_pos = None

        if world.game_pause:
            screen.blit(pause_mask, pause_mask_rect)
            if game_resume_button.draw(screen):
                world.game_pause = not world.game_pause
                game_pause()
            if game_restart_button.draw(screen):
                world.restart(c.HEALTH, c.MONEY)
                speed_up_button.change_image(speed_btn_image[world.game_speed - 1])
                enemy_group.empty()
                tower_group.empty()
            if game_end_button.draw(screen):
                world.game_over = True

        # event
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and not world.game_pause:
                mouse_pos = pg.mouse.get_pos()
                if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                    selected_tower_type = None
                    clear_selection()
                    clean_range_only_tower()
                    selected_tower, selected_tower_pos = select_tower(mouse_pos)
                    if selected_tower is None:
                        selected_tile = select_tile(mouse_pos)
                    else:
                        selected_tile = None
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    world.game_pause = not world.game_pause
                    game_pause()
                if event.key == pg.K_SPACE and not wave_started:
                    world.wave += 1
                    wave_started = True
        pg.display.flip()


def menu():
    # load images
    select_level_image = pg.image.load('assets/buttons/select_level.png').convert_alpha()
    research_image = pg.image.load('assets/buttons/research.png').convert_alpha()
    settings_image = pg.image.load('assets/buttons/settings.png').convert_alpha()
    exit_image = pg.image.load('assets/buttons/exit.png').convert_alpha()

    select_level_button = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) // 2 - 60, 620, select_level_image)
    research_button = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) // 2 - 60, 700, research_image)
    settings_button = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) // 2 - 60, 780, settings_image)
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
        if settings_button.draw(screen):
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
    level_json_data = [x for x in os.listdir('assets/level') if x.endswith(".tmj")]
    level_map_data = [x for x in os.listdir('assets/level') if x.endswith(".png")]

    run = True
    while run:
        clock.tick(c.FPS)

        screen.fill((0, 0, 0))

        draw_text('Level Select', title_font, "grey100", (c.SCREEN_WIDTH + c.SIDE_PANEL) // 2, 100, center=True)

        if arrow_back_button.draw(screen):
            run = False

        for i in range(len(level_json_data)):
            x = 252 + (i % 10) * 84
            y = 252 + (i // 10) * 84
            level_button.change_pos(x, y, True)
            if level_button.draw(screen) and level_json_data[i][:-4] == level_map_data[i][:-4]:
                with open(f'assets/level/{level_json_data[i]}') as f:
                    level_data = json.load(f)
                    play_level(f'assets/level/{level_map_data[i]}', level_data, c.HEALTH, c.MONEY)
            draw_text(str(i + 1), text_font, "grey100", x, y, center=True)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        pg.display.flip()


menu()
pg.quit()
