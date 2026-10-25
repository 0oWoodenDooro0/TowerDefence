import pygame as pg
import src.data.constants as c
from src.core.asset_manager import AssetManager
from src.core.save_manager import SaveManager
from src.scenes.scene_manager import SceneManager
from src.scenes.menu_scene import MainMenuScene
from src.scenes.level_select_scene import LevelSelectScene
from src.scenes.research_scene import ResearchScene
from src.scenes.gameplay_scene import GameplayScene


class GameApp:
    """Main application orchestrator initializing display, assets, and the scene loop."""

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANEL, c.SCREEN_HEIGHT))
        pg.display.set_caption(c.TITLE)
        self.clock = pg.time.Clock()

        self.assets = AssetManager()
        self.save_manager = SaveManager()
        self.scene_manager = SceneManager(self.assets, self.save_manager)

        self.scene_manager.register("menu", MainMenuScene(self.scene_manager))
        self.scene_manager.register("level_select", LevelSelectScene(self.scene_manager))
        self.scene_manager.register("research", ResearchScene(self.scene_manager))
        self.scene_manager.register("gameplay", GameplayScene(self.scene_manager))

        self.scene_manager.switch_to("menu")

    def run(self):
        while self.scene_manager.running:
            dt = self.clock.tick(c.FPS) / 1000.0

            events = pg.event.get()
            self.scene_manager.handle_events(events)
            self.scene_manager.update(dt)
            self.scene_manager.draw(self.screen)

            pg.display.flip()

        pg.quit()
