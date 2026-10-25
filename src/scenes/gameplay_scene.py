import pygame as pg
from src.scenes.base_scene import Scene
from src.core.world import World
from src.entities.tower import Tower, AttackTower, EffectTower, RangeOnlyTower
from src.entities.enemy import Enemy
from src.ui.button import Button
from src.ui.text_renderer import draw_text
from src.data.tower_data import TOWER_TYPE_DATA, TOWER_DATA, TOWER_NAME
import src.data.constants as c


class GameplayScene(Scene):
    """Active gameplay scene managing battlefield simulation, tower building, and wave combat."""

    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.text_font = self.assets.get_font("assets/DigitalDisco-Thin.ttf", 24)

        # Asset surfaces
        self.coin_image = self.assets.get_image("assets/image/coin.png")
        self.coin_rect = self.coin_image.get_rect(center=(592, 522))

        self.selected_tower_image = self.assets.get_image("assets/image/selected_tower.png")
        self.selected_tile_image = self.assets.get_image("assets/image/selected_tile.png")
        self.selected_tower_rect = self.selected_tower_image.get_rect()
        self.selected_tile_rect = self.selected_tile_image.get_rect()

        self.buy_tower_image = self.assets.get_image("assets/buttons/buy_tower.png")
        self.buy_tower_not_enabled_image = self.assets.get_image("assets/buttons/buy_tower_not_enabled.png")
        self.upgrade_tower_image = self.assets.get_image("assets/buttons/upgrade_tower.png")
        self.upgrade_tower_not_enabled_image = self.assets.get_image("assets/buttons/upgrade_tower_not_enabled.png")
        self.start_image = self.assets.get_image("assets/buttons/start.png")
        self.sell_image = self.assets.get_image("assets/buttons/sell.png")
        self.pause_image = self.assets.get_image("assets/buttons/pause.png")
        self.resume_image = self.assets.get_image("assets/buttons/resume.png")

        self.game_pause_image = self.assets.get_image("assets/buttons/game_pause.png")
        self.game_resume_image = self.assets.get_image("assets/buttons/game_resume.png")
        self.game_restart_image = self.assets.get_image("assets/buttons/game_restart.png")
        self.game_end_image = self.assets.get_image("assets/buttons/game_end.png")

        self.speed_btn_images = self.assets.get_speed_button_images()
        self.tower_btn_images = self.assets.get_tower_button_images()

        self.tower_images = self.assets.get_tower_images()
        self.tower_base_images = self.assets.get_tower_base_images()
        self.enemy_images = self.assets.get_enemy_images()

        # UI Overlays
        self.pause_mask = pg.Surface((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
        self.pause_mask.fill((0, 0, 0))
        self.pause_mask.set_alpha(100)
        self.pause_mask_rect = self.pause_mask.get_rect(topleft=(0, 0))

        self.reward_surface = pg.Surface((200, 150))
        self.reward_surface.fill((60, 60, 60))
        self.reward_surface_rect = self.reward_surface.get_rect(center=((c.SCREEN_WIDTH + c.SIDE_PANEL) // 2, 500))

        # Buttons
        self.buy_tower_btn = Button(c.SCREEN_WIDTH + 20, c.SCREEN_HEIGHT - 60, self.buy_tower_image, True, True)
        self.start_btn = Button(c.SCREEN_WIDTH + 20, (c.SCREEN_HEIGHT - 30) // 2 + 100, self.start_image)
        self.sell_btn = Button(c.SCREEN_WIDTH + c.SIDE_PANEL - 140, c.SCREEN_HEIGHT - 60, self.sell_image)
        self.game_pause_btn = Button(42, 42, self.game_pause_image, center=True)
        self.game_resume_btn = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) // 2 - 60, 700, self.game_resume_image)
        self.game_restart_btn = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) // 2 - 60, 780, self.game_restart_image)
        self.game_end_btn = Button((c.SCREEN_WIDTH + c.SIDE_PANEL) // 2 - 60, 860, self.game_end_image)
        self.speed_up_btn = Button(c.SCREEN_WIDTH + c.SIDE_PANEL - 140, (c.SCREEN_HEIGHT - 30) // 2 + 100, self.speed_btn_images[0])

        self.tower_btns = [
            Button(c.SCREEN_WIDTH + 15 + (i % 3) * 95, (c.SCREEN_HEIGHT - 30) // 2 + 190 + (i // 3) * 95, self.tower_btn_images[i])
            for i in range(4)
        ]

        # Runtime state
        self.world: World | None = None
        self.enemy_group = pg.sprite.Group()
        self.tower_group = pg.sprite.Group()
        self.bullet_group = pg.sprite.Group()

        self.wave_started: bool = False
        self.selected_tower: Tower | None = None
        self.selected_tile: tuple | None = None
        self.selected_tower_type: str | None = None
        self.selected_tower_pos: tuple | None = None
        self.level: int = 1
        self.bonus = None

    def on_enter(self, level: int = 1, map_path: str = "assets/level/level1.png", level_data: dict | None = None, **kwargs):
        self.level = level
        self.bonus = self.save_manager.get_bonus()
        map_image = self.assets.get_image(map_path)
        if level_data is None:
            level_data = self.assets.get_map_data("assets/level/level1.tmj")

        self.world = World(map_image, level_data, c.HEALTH, c.MONEY, pg.time.get_ticks(), self.level, self.bonus)
        self.enemy_group.empty()
        self.tower_group.empty()
        self.bullet_group.empty()

        self.wave_started = False
        self.selected_tower = None
        self.selected_tile = None
        self.selected_tower_type = None
        self.selected_tower_pos = None
        self.speed_up_btn.change_image(self.speed_btn_images[0])

    def create_tower(self, tile_pos, range_only=False):
        if range_only:
            new_tower = RangeOnlyTower(self.tower_images, self.tower_base_images, self.selected_tower_type, tile_pos, self.bonus)
        else:
            match self.selected_tower_type:
                case "basic" | "sniper" | "cannon":
                    new_tower = AttackTower(self.tower_images, self.tower_base_images, self.selected_tower_type, tile_pos, self.bonus)
                case "freeze":
                    new_tower = EffectTower(self.tower_images, self.tower_base_images, self.selected_tower_type, tile_pos, self.bonus)
                case _:
                    new_tower = None
        self.tower_group.add(new_tower)
        return new_tower, tile_pos

    def select_tile(self, pos):
        mouse_tile_x = pos[0] // c.TILE_SIZE
        mouse_tile_y = pos[1] // c.TILE_SIZE
        mouse_tile_num = (mouse_tile_y * c.COLS) + mouse_tile_x
        for tower_id in self.world.tower_tile_id:
            if self.world.tile_map[mouse_tile_num] == tower_id:
                space_is_free = True
                for t in self.tower_group:
                    if (mouse_tile_x, mouse_tile_y) == (t.tile_x, t.tile_y):
                        space_is_free = False
                if space_is_free:
                    return mouse_tile_x, mouse_tile_y
        return None

    def select_tower(self, pos):
        mouse_tile_x = pos[0] // c.TILE_SIZE
        mouse_tile_y = pos[1] // c.TILE_SIZE
        for t in self.tower_group:
            if (mouse_tile_x, mouse_tile_y) == (t.tile_x, t.tile_y):
                return t, (mouse_tile_x, mouse_tile_y)
        return None, None

    def clear_selection(self):
        for t in self.tower_group:
            t.selected = False

    def clean_range_only_tower(self):
        for t in self.tower_group:
            if type(t) == RangeOnlyTower:
                t.kill()

    def game_pause_toggle(self):
        self.world.pause(pg.time.get_ticks())
        for t in self.tower_group:
            if type(t) is AttackTower:
                t.pause(pg.time.get_ticks(), self.world)

    def get_attribute(self, tower_type: str, attribute: str, is_bonus: bool = True):
        return TOWER_DATA[tower_type][0].get(attribute) * self.bonus.get_bonus_data(attribute) if is_bonus else TOWER_DATA[tower_type][0].get(attribute)

    def restart(self):
        final_reward = round(self.world.reward * self.world.bonus.get_bonus_data("coin_bonus"))
        self.save_manager.add_coin_reward(final_reward)
        self.world.reward = 0
        self.world.restart(c.HEALTH, c.MONEY)
        self.speed_up_btn.change_image(self.speed_btn_images[self.world.game_speed - 1])
        self.enemy_group.empty()
        self.tower_group.empty()

    def end_game(self):
        final_reward = round(self.world.reward * self.world.bonus.get_bonus_data("coin_bonus"))
        self.save_manager.add_coin_reward(final_reward)
        self.world.reward = 0
        self.world.game_over = True
        self.manager.switch_to("menu")

    def handle_event(self, event: pg.event.Event):
        if not self.world:
            return

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and not self.world.game_pause:
            mouse_pos = pg.mouse.get_pos()
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                self.selected_tower_type = None
                self.clear_selection()
                self.clean_range_only_tower()
                self.selected_tower, self.selected_tower_pos = self.select_tower(mouse_pos)
                if self.selected_tower is None:
                    self.selected_tile = self.select_tile(mouse_pos)
                else:
                    self.selected_tile = None

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.world.game_pause = not self.world.game_pause
                self.game_pause_toggle()
            if event.key == pg.K_SPACE and not self.wave_started:
                self.wave_started = True

    def update(self, dt: float = 0.0):
        if not self.world:
            return

        self.world.update()
        if not self.world.game_over and not self.world.run_pause and not self.world.game_pause:
            self.enemy_group.update(self.world)
            self.bullet_group.update(self.world, self.enemy_group)
            self.tower_group.update(self.enemy_group, self.bullet_group, self.world)

            if self.selected_tower:
                self.selected_tower.selected = True

            if self.wave_started:
                if pg.time.get_ticks() - self.world.last_enemy_spawn > self.world.spawn_cooldown / self.world.game_speed:
                    if self.world.spawned_enemies < len(self.world.enemy_list):
                        enemy_type = self.world.enemy_list[self.world.spawned_enemies]
                        enemy = Enemy(enemy_type, self.world.waypoints, self.enemy_images, self.world.wave, self.world.level)
                        self.enemy_group.add(enemy)
                        self.world.spawned_enemies += 1
                        self.world.last_enemy_spawn = pg.time.get_ticks()

            if self.world.check_wave_completed():
                self.world.reward = int(self.world.reward + 10 * self.world.wave * (1 + (self.world.level - 1) * 0.2))
                self.world.wave += 1
                self.wave_started = False
                self.world.last_enemy_spawn = pg.time.get_ticks()
                self.world.reset_wave()
                self.world.process_enemies()

    def draw(self, surface: pg.Surface):
        if not self.world:
            return

        surface.fill("grey100")
        self.world.draw(surface)

        self.enemy_group.draw(surface)
        for enemy in self.enemy_group:
            enemy.health_bar.draw(surface)
        for tower in self.tower_group:
            tower.draw(surface)
        self.bullet_group.draw(surface)

        # In-battle HUD (Uses Money, not Coin)
        draw_text(surface, f"Health: {self.world.health}", self.text_font, "black", c.SCREEN_WIDTH + 5, 0)
        draw_text(surface, f"Money: {self.world.money}", self.text_font, "black", c.SCREEN_WIDTH + 5, 30)
        draw_text(surface, f"Wave: {self.world.wave}", self.text_font, "black", c.SCREEN_WIDTH + 5, 60)

        if self.game_pause_btn.draw(surface) and not self.world.game_pause:
            self.world.game_pause = not self.world.game_pause
            self.game_pause_toggle()

        if not self.world.game_over:
            if self.speed_up_btn.draw(surface) and not self.world.game_pause:
                self.world.update_speed()
                self.world.last_enemy_spawn = (pg.time.get_ticks() - self.world.last_enemy_spawn) / self.world.game_speed + self.world.last_enemy_spawn
                self.speed_up_btn.change_image(self.speed_btn_images[self.world.game_speed - 1])

            if not self.wave_started:
                draw_text(surface, f"Enemy Type: {self.world.next_wave_enemies_type}", self.text_font, "black", c.SCREEN_WIDTH + 5, 350)
                draw_text(surface, f"Num of Enemy : {self.world.next_wave_enemies_num}", self.text_font, "black", c.SCREEN_WIDTH + 5, 380)
                self.start_btn.change_image(self.start_image)
                if self.start_btn.draw(surface):
                    self.wave_started = True
            else:
                if self.world.run_pause:
                    self.start_btn.change_image(self.resume_image)
                else:
                    self.start_btn.change_image(self.pause_image)
                if self.start_btn.draw(surface) and not self.world.game_pause:
                    self.world.run_pause = not self.world.run_pause
                    self.game_pause_toggle()

            if self.selected_tile:
                for i in range(4):
                    if self.tower_btns[i].draw(surface):
                        self.selected_tower_type = TOWER_NAME[i]
                        self.clean_range_only_tower()
                        self.selected_tower, _ = self.create_tower(self.selected_tile, True)
                        self.selected_tower_pos = (c.SCREEN_WIDTH + (i % 3) * 95 + 55, (c.SCREEN_HEIGHT - 30) // 2 + (i // 3) * 95 + 230)

                self.selected_tile_rect.center = ((self.selected_tile[0] + 0.5) * c.TILE_SIZE, (self.selected_tile[1] + 0.5) * c.TILE_SIZE)
                surface.blit(self.selected_tile_image, self.selected_tile_rect)

                if self.selected_tower_type is not None:
                    self.selected_tower_rect.center = self.selected_tower_pos
                    surface.blit(self.selected_tower_image, self.selected_tower_rect)
                    draw_text(surface, f"Tower Type: {self.selected_tower_type}", self.text_font, "black", c.SCREEN_WIDTH + 5, 150)
                    match self.selected_tower_type:
                        case "basic" | "sniper" | "cannon":
                            draw_text(surface, f"damage: {round(self.get_attribute(self.selected_tower_type, 'damage'), 2)}", self.text_font, "black", c.SCREEN_WIDTH + 5, 180)
                            draw_text(surface, f"attack speed: {round(self.get_attribute(self.selected_tower_type, 'atk_speed'), 2)}", self.text_font, "black", c.SCREEN_WIDTH + 5, 210)
                            draw_text(surface, f"range: {round(self.get_attribute(self.selected_tower_type, 'range'), 2)}", self.text_font, "black", c.SCREEN_WIDTH + 5, 240)
                        case "freeze":
                            draw_text(surface, f"slow rate: {1 - self.get_attribute(self.selected_tower_type, 'slow_rate', False) :.2f}", self.text_font, "black", c.SCREEN_WIDTH + 5, 180)
                            draw_text(surface, f"range: {round(self.get_attribute(self.selected_tower_type, 'range'), 2)}", self.text_font, "black", c.SCREEN_WIDTH + 5, 210)

                    tower_cost = TOWER_TYPE_DATA[self.selected_tower_type].get("cost")
                    draw_text(surface, f"Cost: {tower_cost}", self.text_font, "black", c.SCREEN_WIDTH + 30, c.SCREEN_HEIGHT - 110)
                    if self.world.money >= tower_cost:
                        self.buy_tower_btn.change_image(self.buy_tower_image)
                        if self.buy_tower_btn.draw(surface)[0]:
                            self.clean_range_only_tower()
                            self.selected_tower, self.selected_tower_pos = self.create_tower(self.selected_tile)
                            self.world.money -= tower_cost
                            self.selected_tile = None
                    else:
                        self.buy_tower_btn.change_image(self.buy_tower_not_enabled_image)
                        self.buy_tower_btn.draw(surface)

            elif self.selected_tower:
                self.selected_tower.selected = True
                self.selected_tile_rect.center = ((self.selected_tower_pos[0] + 0.5) * c.TILE_SIZE, (self.selected_tower_pos[1] + 0.5) * c.TILE_SIZE)
                surface.blit(self.selected_tile_image, self.selected_tile_rect)
                draw_text(surface, f"Tower Type: {self.selected_tower.tower_type}", self.text_font, "black", c.SCREEN_WIDTH + 5, 150)

                if self.selected_tower.level < len(TOWER_DATA[self.selected_tower.tower_type]):
                    draw_text(surface, f"Cost: {self.selected_tower.cost}", self.text_font, "black", c.SCREEN_WIDTH + 30, c.SCREEN_HEIGHT - 110)
                    match self.selected_tower.tower_type:
                        case "basic" | "sniper" | "cannon":
                            draw_text(surface, f"damage: {round(self.selected_tower.get_attribute(self.selected_tower.level - 1, 'damage'), 2)} -> {round(self.selected_tower.get_attribute(self.selected_tower.level, 'damage'), 2)}", self.text_font, "black", c.SCREEN_WIDTH + 5, 180)
                            draw_text(surface, f"range: {round(self.selected_tower.get_attribute(self.selected_tower.level - 1, 'range'), 2)} -> {round(self.selected_tower.get_attribute(self.selected_tower.level, 'range'), 2)}", self.text_font, "black", c.SCREEN_WIDTH + 5, 210)
                            draw_text(surface, f"attack speed: {round(self.selected_tower.get_attribute(self.selected_tower.level - 1, 'atk_speed'), 2)} -> {round(self.selected_tower.get_attribute(self.selected_tower.level, 'atk_speed'), 2)}", self.text_font, "black", c.SCREEN_WIDTH + 5, 240)
                        case "freeze":
                            draw_text(surface, f"slow rate: {1 - self.selected_tower.get_attribute(self.selected_tower.level - 1, 'slow_rate'):.2f} -> {1 - self.selected_tower.get_attribute(self.selected_tower.level, 'slow_rate'):.2f}", self.text_font, "black", c.SCREEN_WIDTH + 5, 180)
                            draw_text(surface, f"range: {round(self.selected_tower.get_attribute(self.selected_tower.level - 1, 'range'), 2)} -> {round(self.selected_tower.get_attribute(self.selected_tower.level, 'range'), 2)}", self.text_font, "black", c.SCREEN_WIDTH + 5, 210)

                    if self.world.money >= self.selected_tower.cost:
                        self.buy_tower_btn.change_image(self.upgrade_tower_image)
                        btn_clicked = self.buy_tower_btn.draw(surface)
                        if btn_clicked[0]:
                            self.world.money -= self.selected_tower.cost
                            self.selected_tower.upgrade()
                        elif btn_clicked[1]:
                            self.selected_tower.check_range = True
                        else:
                            self.selected_tower.check_range = False
                    else:
                        self.buy_tower_btn.change_image(self.upgrade_tower_not_enabled_image)
                        btn_clicked = self.buy_tower_btn.draw(surface)
                        if btn_clicked[1]:
                            self.selected_tower.check_range = True
                        else:
                            self.selected_tower.check_range = False
                else:
                    match self.selected_tower.tower_type:
                        case "basic" | "sniper" | "cannon":
                            draw_text(surface, f"damage: {round(self.selected_tower.get_attribute(self.selected_tower.level - 1, 'damage'), 2)}", self.text_font, "black", c.SCREEN_WIDTH + 5, 180)
                            draw_text(surface, f"range: {round(self.selected_tower.get_attribute(self.selected_tower.level - 1, 'range'), 2)}", self.text_font, "black", c.SCREEN_WIDTH + 5, 210)
                            draw_text(surface, f"attack speed: {round(self.selected_tower.get_attribute(self.selected_tower.level - 1, 'atk_speed'), 2)}", self.text_font, "black", c.SCREEN_WIDTH + 5, 240)
                        case "freeze":
                            draw_text(surface, f"slow rate: {1 - self.selected_tower.get_attribute(self.selected_tower.level - 1, 'slow_rate'):.2f}", self.text_font, "black", c.SCREEN_WIDTH + 5, 180)
                            draw_text(surface, f"range: {round(self.selected_tower.get_attribute(self.selected_tower.level - 1, 'range'), 2)}", self.text_font, "black", c.SCREEN_WIDTH + 5, 210)

                draw_text(surface, f"SELL: {self.selected_tower.sell}", self.text_font, "black", c.SCREEN_WIDTH + 170, c.SCREEN_HEIGHT - 110)
                if self.sell_btn.draw(surface):
                    self.world.money += self.selected_tower.sell
                    self.tower_group.remove(self.selected_tower)
                    self.selected_tower = None
        else:
            self.selected_tower = None
            self.selected_tile = None
            self.selected_tower_type = None
            self.selected_tower_pos = None

            surface.blit(self.pause_mask, self.pause_mask_rect)
            surface.blit(self.reward_surface, self.reward_surface_rect)
            surface.blit(self.coin_image, self.coin_rect)
            draw_text(surface, "Reward", self.text_font, (255, 255, 255), 630, 450, center=True)
            reward_amt = round(self.world.reward * self.world.bonus.get_bonus_data("coin_bonus"))
            draw_text(surface, f"{reward_amt}", self.text_font, (255, 255, 255), 650, 522, center=True)

            if self.game_restart_btn.draw(surface):
                self.restart()
            if self.game_end_btn.draw(surface):
                self.end_game()

        if self.world.game_pause:
            surface.blit(self.pause_mask, self.pause_mask_rect)
            surface.blit(self.reward_surface, self.reward_surface_rect)
            surface.blit(self.coin_image, self.coin_rect)
            draw_text(surface, "Reward", self.text_font, (255, 255, 255), 630, 450, center=True)
            reward_amt = round(self.world.reward * self.world.bonus.get_bonus_data("coin_bonus"))
            draw_text(surface, f"{reward_amt}", self.text_font, (255, 255, 255), 650, 522, center=True)

            if self.game_resume_btn.draw(surface):
                self.world.game_pause = not self.world.game_pause
                self.game_pause_toggle()
            if self.game_restart_btn.draw(surface):
                self.restart()
            if self.game_end_btn.draw(surface):
                self.end_game()
