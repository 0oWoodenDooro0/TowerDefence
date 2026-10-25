import pygame as pg
from src.scenes.base_scene import Scene
from src.ui.button import Button
from src.ui.text_renderer import draw_text
import src.data.constants as c


class MainMenuScene(Scene):
    """Main menu scene providing navigation to level selection and research."""

    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        center_x = (c.SCREEN_WIDTH + c.SIDE_PANEL) // 2

        self.coin_image = self.assets.get_image("assets/image/coin.png")
        self.coin_rect = self.coin_image.get_rect(topleft=(1000, 10))

        self.select_level_btn = Button(
            center_x - 60, 620,
            self.assets.get_image("assets/buttons/select_level.png")
        )
        self.research_btn = Button(
            center_x - 60, 700,
            self.assets.get_image("assets/buttons/research.png")
        )
        self.settings_btn = Button(
            center_x - 60, 780,
            self.assets.get_image("assets/buttons/settings.png")
        )
        self.exit_btn = Button(
            center_x - 60, 860,
            self.assets.get_image("assets/buttons/exit.png")
        )

        self.title_font = self.assets.get_font("assets/DigitalDisco-Thin.ttf", 100)
        self.text_font = self.assets.get_font("assets/DigitalDisco-Thin.ttf", 24)
        self.coin: int = 0

    def on_enter(self, **kwargs):
        data = self.save_manager.load_data()
        self.coin = data.get("coin", 0)

    def handle_event(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.manager.quit()

    def update(self, dt: float = 0.0):
        pass

    def draw(self, surface: pg.Surface):
        surface.fill((0, 0, 0))

        center_x = (c.SCREEN_WIDTH + c.SIDE_PANEL) // 2
        draw_text(surface, "Tower Defense", self.title_font, "grey100", center_x, 200, center=True)

        surface.blit(self.coin_image, self.coin_rect)
        draw_text(surface, f"{self.coin}", self.text_font, "grey100", 1080, 32)

        if self.select_level_btn.draw(surface):
            self.manager.switch_to("level_select")
        elif self.research_btn.draw(surface):
            self.manager.switch_to("research")
        elif self.settings_btn.draw(surface):
            pass
        elif self.exit_btn.draw(surface):
            self.manager.quit()
