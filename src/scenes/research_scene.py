import pygame as pg
from src.scenes.base_scene import Scene
from src.ui.button import Button
from src.ui.text_renderer import draw_text
from src.data.research_data import RESEARCH


class ResearchScene(Scene):
    """Research laboratory scene for upgrading permanent global Bonus levels using Coins."""

    BONUS_ATTRIBUTES = [
        "starting_money_bonus", "starting_health_bonus", "rotate_speed",
        "damage", "range", "atk_speed", "sell", "cost", "coin_bonus"
    ]

    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.text_font = self.assets.get_font("assets/DigitalDisco-Thin.ttf", 24)

        self.coin_image = self.assets.get_image("assets/image/coin.png")
        self.coin_rect = self.coin_image.get_rect(topleft=(1000, 10))

        self.arrow_back_btn = Button(
            100, 100,
            self.assets.get_image("assets/buttons/arrow_back.png"),
            center=True
        )
        self.level_btn = Button(
            0, 0,
            self.assets.get_image("assets/buttons/level.png")
        )
        self.data: dict = {}
        self.coin: int = 0

    def on_enter(self, **kwargs):
        self.data = self.save_manager.load_data()
        self.coin = self.data.get("coin", 0)

    def handle_event(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.manager.switch_to("menu")

    def draw(self, surface: pg.Surface):
        surface.fill((0, 0, 0))

        surface.blit(self.coin_image, self.coin_rect)
        draw_text(surface, f"{self.coin}", self.text_font, "grey100", 1080, 32)

        if self.arrow_back_btn.draw(surface):
            self.manager.switch_to("menu")
            return

        for i, attr in enumerate(self.BONUS_ATTRIBUTES):
            x = 299 + (i % 3) * 331
            y = 250 + (i // 3) * 200
            self.level_btn.change_pos(x, y, True)

            level = self.data.get(attr, 0)
            cost = RESEARCH[attr][level]["cost"]

            if self.level_btn.draw(surface) and self.coin >= cost and level < 5:
                if self.save_manager.upgrade_research(attr, cost):
                    self.data = self.save_manager.load_data()
                    self.coin = self.data.get("coin", 0)
                    level = self.data.get(attr, 0)

            draw_text(surface, f"{level}", self.text_font, "grey100", x, y, center=True)
            draw_text(surface, attr, self.text_font, "grey100", x, y + 60, center=True)
            draw_text(surface, RESEARCH[attr][level]["description"], self.text_font, "grey100", x, y + 90, center=True)
            if level < 5:
                draw_text(surface, f"cost: {cost}", self.text_font, "grey100", x, y + 120, center=True)
