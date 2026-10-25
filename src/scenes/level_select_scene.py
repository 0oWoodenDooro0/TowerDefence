import os
import pygame as pg
from src.scenes.base_scene import Scene
from src.ui.button import Button
from src.ui.text_renderer import draw_text
import src.data.constants as c


class LevelSelectScene(Scene):
    """Level selection scene listing available battle stages."""

    def __init__(self, scene_manager):
        super().__init__(scene_manager)
        self.title_font = self.assets.get_font("assets/DigitalDisco-Thin.ttf", 100)
        self.text_font = self.assets.get_font("assets/DigitalDisco-Thin.ttf", 24)

        self.arrow_back_btn = Button(
            100, 100,
            self.assets.get_image("assets/buttons/arrow_back.png"),
            center=True
        )
        self.level_btn = Button(
            0, 0,
            self.assets.get_image("assets/buttons/level.png")
        )

        level_dir = "assets/level"
        self.level_json_files = sorted([x for x in os.listdir(level_dir) if x.endswith(".tmj")])
        self.level_map_files = sorted([x for x in os.listdir(level_dir) if x.endswith(".png")])

    def handle_event(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self.manager.switch_to("menu")

    def draw(self, surface: pg.Surface):
        surface.fill((0, 0, 0))

        center_x = (c.SCREEN_WIDTH + c.SIDE_PANEL) // 2
        draw_text(surface, "Level Select", self.title_font, "grey100", center_x, 100, center=True)

        if self.arrow_back_btn.draw(surface):
            self.manager.switch_to("menu")
            return

        for i, json_file in enumerate(self.level_json_files):
            x = 252 + (i % 10) * 84
            y = 252 + (i // 10) * 84
            self.level_btn.change_pos(x, y, True)

            map_file = self.level_map_files[i] if i < len(self.level_map_files) else None
            if self.level_btn.draw(surface) and map_file and json_file[:-4] == map_file[:-4]:
                map_path = f"assets/level/{map_file}"
                level_data = self.assets.get_map_data(f"assets/level/{json_file}")
                self.manager.switch_to("gameplay", level=i + 1, map_path=map_path, level_data=level_data)
                return

            draw_text(surface, str(i + 1), self.text_font, "grey100", x, y, center=True)
