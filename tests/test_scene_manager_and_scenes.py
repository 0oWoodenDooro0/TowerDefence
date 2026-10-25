import pygame as pg
import pytest
from src.scenes.scene_manager import SceneManager
from src.scenes.base_scene import Scene
from src.scenes.menu_scene import MainMenuScene
from src.scenes.level_select_scene import LevelSelectScene
from src.scenes.research_scene import ResearchScene
from src.core.save_manager import SaveManager
from src.core.asset_manager import AssetManager


class DummyScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.entered = False
        self.exited = False

    def on_enter(self, **kwargs):
        self.entered = True

    def on_exit(self):
        self.exited = True


def test_scene_manager_registration_and_switching():
    manager = SceneManager()
    dummy1 = DummyScene(manager)
    dummy2 = DummyScene(manager)

    manager.register("scene1", dummy1)
    manager.register("scene2", dummy2)

    manager.switch_to("scene1")
    assert manager.active_scene_name == "scene1"
    assert dummy1.entered is True

    manager.switch_to("scene2")
    assert dummy1.exited is True
    assert manager.active_scene_name == "scene2"
    assert dummy2.entered is True


def test_scene_manager_quit_event():
    manager = SceneManager()
    dummy = DummyScene(manager)
    manager.register("dummy", dummy)
    manager.switch_to("dummy")

    assert manager.running is True
    quit_event = pg.event.Event(pg.QUIT)
    manager.handle_events([quit_event])
    assert manager.running is False


def test_menu_scene_lifecycle(tmp_path):
    save_file = str(tmp_path / "data.json")
    save_manager = SaveManager(save_file)
    save_manager.add_coin_reward(300)

    manager = SceneManager(save_manager=save_manager)
    menu_scene = MainMenuScene(manager)
    manager.register("menu", menu_scene)

    manager.switch_to("menu")
    assert menu_scene.coin == 300

    # Draw to headless surface without crashing
    surface = pg.Surface((1260, 960))
    menu_scene.draw(surface)


def test_research_scene_upgrade_integration(tmp_path):
    save_file = str(tmp_path / "data.json")
    save_manager = SaveManager(save_file)
    save_manager.add_coin_reward(1500)

    manager = SceneManager(save_manager=save_manager)
    research_scene = ResearchScene(manager)
    manager.register("research", research_scene)

    manager.switch_to("research")
    assert research_scene.coin == 1500

    # Simulate purchase directly through save_manager as button click would trigger
    cost = 750
    assert save_manager.upgrade_research("starting_money_bonus", cost) is True

    # Re-entering or updating reflects new balance
    research_scene.on_enter()
    assert research_scene.coin == 750
    assert research_scene.data["starting_money_bonus"] == 1
