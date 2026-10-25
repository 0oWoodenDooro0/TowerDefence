import json
import os
import pygame as pg


class AssetManager:
    """Centralized asset loader and in-memory cache for textures, fonts, and level data."""

    def __init__(self, base_path: str = "assets"):
        self.base_path = base_path
        self._images: dict[str, pg.Surface] = {}
        self._fonts: dict[tuple[str, int], pg.font.Font] = {}
        self._map_data: dict[str, dict] = {}

    def get_image(self, rel_or_abs_path: str) -> pg.Surface:
        """Loads an image if not cached, and returns the cached Surface."""
        path = rel_or_abs_path
        if not os.path.isabs(path) and not path.startswith(self.base_path):
            path = os.path.join(self.base_path, rel_or_abs_path)

        if path in self._images:
            return self._images[path]

        if not os.path.exists(path):
            raise FileNotFoundError(f"Asset image not found: {path}")

        raw_surf = pg.image.load(path)
        try:
            surface = raw_surf.convert_alpha()
        except pg.error:
            surface = raw_surf

        self._images[path] = surface
        return surface

    def get_font(self, font_path: str, size: int) -> pg.font.Font:
        """Loads a font at the specified size with in-memory caching."""
        path = font_path
        if not os.path.isabs(path) and not path.startswith(self.base_path):
            path = os.path.join(self.base_path, font_path)

        key = (path, size)
        if key in self._fonts:
            return self._fonts[key]

        if not os.path.exists(path):
            font = pg.font.Font(None, size)
        else:
            font = pg.font.Font(path, size)

        self._fonts[key] = font
        return font

    def get_map_data(self, path: str) -> dict:
        """Loads and caches map JSON/TMJ data."""
        if path in self._map_data:
            return self._map_data[path]

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self._map_data[path] = data
        return data

    def get_tower_images(self) -> dict[str, pg.Surface]:
        return {
            "basic": self.get_image("assets/tower/tower1.png"),
            "sniper": self.get_image("assets/tower/tower2.png"),
            "cannon": self.get_image("assets/tower/tower3.png"),
            "freeze": self.get_image("assets/tower/tower4.png"),
        }

    def get_tower_base_images(self) -> dict[str, pg.Surface]:
        return {
            "basic": self.get_image("assets/tower/tower_base1.png"),
            "sniper": self.get_image("assets/tower/tower_base2.png"),
            "cannon": self.get_image("assets/tower/tower_base3.png"),
            "freeze": self.get_image("assets/tower/tower_base4.png"),
        }

    def get_enemy_images(self) -> dict[str, pg.Surface]:
        return {
            "regular": self.get_image("assets/enemy/enemy1.png"),
            "fast": self.get_image("assets/enemy/enemy2.png"),
            "strong": self.get_image("assets/enemy/enemy3.png"),
        }

    def get_speed_button_images(self) -> list[pg.Surface]:
        return [
            self.get_image("assets/buttons/speed1x.png"),
            self.get_image("assets/buttons/speed2x.png"),
            self.get_image("assets/buttons/speed3x.png"),
        ]

    def get_tower_button_images(self) -> list[pg.Surface]:
        return [
            self.get_image("assets/buttons/tower1_btn.png"),
            self.get_image("assets/buttons/tower2_btn.png"),
            self.get_image("assets/buttons/tower3_btn.png"),
            self.get_image("assets/buttons/tower4_btn.png"),
        ]
