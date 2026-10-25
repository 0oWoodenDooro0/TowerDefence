import pygame as pg
from src.core.asset_manager import AssetManager
from src.core.save_manager import SaveManager
from src.scenes.base_scene import Scene


class SceneManager:
    """Manages scene registration, transitions, and main event/update/draw dispatching."""

    def __init__(self, assets: AssetManager | None = None, save_manager: SaveManager | None = None):
        self.assets = assets or AssetManager()
        self.save_manager = save_manager or SaveManager()
        self.scenes: dict[str, Scene] = {}
        self.active_scene: Scene | None = None
        self.active_scene_name: str | None = None
        self.running: bool = True

    def register(self, name: str, scene: Scene):
        self.scenes[name] = scene

    def switch_to(self, name: str, **kwargs):
        if name not in self.scenes:
            raise KeyError(f"Scene '{name}' is not registered.")
        if self.active_scene:
            self.active_scene.on_exit()
        self.active_scene_name = name
        self.active_scene = self.scenes[name]
        self.active_scene.on_enter(**kwargs)

    def handle_events(self, events: list[pg.event.Event]):
        for event in events:
            if event.type == pg.QUIT:
                self.running = False
                return
            if self.active_scene:
                self.active_scene.handle_event(event)

    def update(self, dt: float = 0.0):
        if self.active_scene:
            self.active_scene.update(dt)

    def draw(self, surface: pg.Surface):
        if self.active_scene:
            self.active_scene.draw(surface)

    def quit(self):
        self.running = False
