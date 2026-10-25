import pygame as pg
import pytest
from src.scenes.scene_manager import SceneManager
from src.scenes.gameplay_scene import GameplayScene
from src.scenes.menu_scene import MainMenuScene
from src.core.save_manager import SaveManager
from src.core.asset_manager import AssetManager


def test_gameplay_scene_lifecycle(tmp_path):
    save_file = str(tmp_path / "data.json")
    save_manager = SaveManager(save_file)
    save_manager.add_coin_reward(100)

    manager = SceneManager(save_manager=save_manager)
    menu_scene = MainMenuScene(manager)
    gameplay_scene = GameplayScene(manager)

    manager.register("menu", menu_scene)
    manager.register("gameplay", gameplay_scene)

    manager.switch_to("gameplay", level=1)
    assert manager.active_scene_name == "gameplay"
    assert gameplay_scene.world is not None
    assert gameplay_scene.world.level == 1
    assert gameplay_scene.world.health > 0
    assert gameplay_scene.world.money > 0


def test_gameplay_scene_tower_placement_and_upgrades(tmp_path):
    save_file = str(tmp_path / "data.json")
    save_manager = SaveManager(save_file)

    manager = SceneManager(save_manager=save_manager)
    gameplay_scene = GameplayScene(manager)
    manager.register("gameplay", gameplay_scene)
    manager.switch_to("gameplay", level=1)

    initial_money = gameplay_scene.world.money
    gameplay_scene.selected_tower_type = "basic"
    tower, pos = gameplay_scene.create_tower((2, 2))

    assert tower in gameplay_scene.tower_group
    assert tower.level == 1
    assert tower.damage > 0


def test_gameplay_scene_pause_toggle(tmp_path):
    save_file = str(tmp_path / "data.json")
    save_manager = SaveManager(save_file)

    manager = SceneManager(save_manager=save_manager)
    gameplay_scene = GameplayScene(manager)
    manager.register("gameplay", gameplay_scene)
    manager.switch_to("gameplay", level=1)

    assert gameplay_scene.world.game_pause is False
    # Simulate Escape key
    esc_event = pg.event.Event(pg.KEYDOWN, key=pg.K_ESCAPE)
    gameplay_scene.handle_event(esc_event)
    assert gameplay_scene.world.game_pause is True


def test_gameplay_scene_end_game_persists_rewards(tmp_path):
    save_file = str(tmp_path / "data.json")
    save_manager = SaveManager(save_file)
    initial_coins = save_manager.load_data()["coin"]

    manager = SceneManager(save_manager=save_manager)
    menu_scene = MainMenuScene(manager)
    gameplay_scene = GameplayScene(manager)

    manager.register("menu", menu_scene)
    manager.register("gameplay", gameplay_scene)

    manager.switch_to("gameplay", level=1)
    gameplay_scene.world.reward = 80
    gameplay_scene.end_game()

    # Verify transition back to menu
    assert manager.active_scene_name == "menu"
    # Verify reward added to persistent coin balance
    updated_coins = save_manager.load_data()["coin"]
    assert updated_coins == initial_coins + 80


def test_gameplay_scene_headless_render(tmp_path):
    save_file = str(tmp_path / "data.json")
    save_manager = SaveManager(save_file)

    manager = SceneManager(save_manager=save_manager)
    gameplay_scene = GameplayScene(manager)
    manager.register("gameplay", gameplay_scene)
    manager.switch_to("gameplay", level=1)

    surface = pg.Surface((1260, 960))
    # Should render all layers without crashing
    gameplay_scene.draw(surface)


def test_gameplay_scene_freeze_tower_inspection(tmp_path):
    save_file = str(tmp_path / "data.json")
    save_manager = SaveManager(save_file)

    manager = SceneManager(save_manager=save_manager)
    gameplay_scene = GameplayScene(manager)
    manager.register("gameplay", gameplay_scene)
    manager.switch_to("gameplay", level=1)

    surface = pg.Surface((1260, 960))
    gameplay_scene.selected_tower_type = "freeze"
    tower, pos = gameplay_scene.create_tower((2, 2))

    # Select the freeze tower
    gameplay_scene.selected_tower = tower
    gameplay_scene.selected_tower_pos = pos
    gameplay_scene.selected_tile = None
    gameplay_scene.selected_tower_type = None

    # Base level inspection
    gameplay_scene.draw(surface)

    # Upgrade to max level
    while tower.level < 6:
        tower.upgrade()

    # Max level inspection
    gameplay_scene.draw(surface)
