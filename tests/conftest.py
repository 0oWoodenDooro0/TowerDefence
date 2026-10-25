import os
import json
import pytest

# Force headless video driver for pygame before any pygame import
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame as pg

pg.init()
pg.display.set_mode((1, 1))


class MockBonus:
    def __init__(self, overrides=None):
        self.data = {
            "starting_money_bonus": 0,
            "starting_health_bonus": 0,
            "damage": 0,
            "range": 0,
            "atk_speed": 0,
            "rotate_speed": 0,
            "sell": 0,
            "cost": 0,
            "coin_bonus": 0
        }
        if overrides:
            self.data.update(overrides)

    def get_bonus_data(self, key):
        # Default multiplier for multipliers is 1, bonuses for flat is 0
        if "starting" in key:
            return self.data.get(key, 0)
        return 1.0


@pytest.fixture
def mock_bonus():
    return MockBonus()


@pytest.fixture
def sample_level_data():
    with open("assets/level/level1.tmj") as f:
        return json.load(f)


@pytest.fixture
def headless_surface():
    return pg.Surface((100, 100))
