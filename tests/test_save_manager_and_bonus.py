import os
import pytest
from src.core.save_manager import SaveManager
from src.core.bonus import Bonus
from src.data.constants import DEFAULT_DATA
from src.data.research_data import RESEARCH


def test_save_manager_fallback_on_missing_file(tmp_path):
    save_file = str(tmp_path / "data.json")
    manager = SaveManager(save_file)
    data = manager.load_data()

    assert data["coin"] == 0
    assert data["starting_money_bonus"] == 0
    assert os.path.exists(save_file)


def test_save_manager_adds_coin_reward(tmp_path):
    save_file = str(tmp_path / "data.json")
    manager = SaveManager(save_file)

    data = manager.add_coin_reward(150)
    assert data["coin"] == 150

    # Reload from disk to verify persistence
    reloaded = manager.load_data()
    assert reloaded["coin"] == 150


def test_save_manager_upgrade_research(tmp_path):
    save_file = str(tmp_path / "data.json")
    manager = SaveManager(save_file)
    manager.add_coin_reward(1000)

    # Attempt upgrade with sufficient coins
    success = manager.upgrade_research("starting_money_bonus", 750)
    assert success is True

    data = manager.load_data()
    assert data["coin"] == 250
    assert data["starting_money_bonus"] == 1

    # Attempt upgrade with insufficient coins
    failed = manager.upgrade_research("starting_money_bonus", 800)
    assert failed is False
    assert data["coin"] == 250
    assert data["starting_money_bonus"] == 1


def test_bonus_calculation_parity(tmp_path):
    save_file = str(tmp_path / "data.json")
    manager = SaveManager(save_file)
    manager.add_coin_reward(2000)
    manager.upgrade_research("starting_money_bonus", 750)

    bonus = manager.get_bonus()
    # At level 1, starting_money_bonus description is +10 and bonus is 5
    assert bonus.get_bonus_data("starting_money_bonus") == RESEARCH["starting_money_bonus"][1]["bonus"]
    # At level 0, damage bonus is 0 (or baseline)
    assert bonus.get_bonus_data("damage") == RESEARCH["damage"][0]["bonus"]
