import os
import pygame as pg
import pytest
from src.app import GameApp


def test_game_app_initialization():
    app = GameApp()
    assert app.screen is not None
    assert app.scene_manager.active_scene_name == "menu"
    assert app.scene_manager.running is True

    # Simulate immediate quit event
    quit_event = pg.event.Event(pg.QUIT)
    app.scene_manager.handle_events([quit_event])
    assert app.scene_manager.running is False
