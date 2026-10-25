import os
import pytest
import pygame as pg
from src.core.asset_manager import AssetManager


def test_asset_manager_caches_image():
    assets = AssetManager()
    img1 = assets.get_image("assets/image/coin.png")
    img2 = assets.get_image("assets/image/coin.png")

    assert isinstance(img1, pg.Surface)
    assert img1 is img2  # Must return the same cached instance


def test_asset_manager_raises_file_not_found():
    assets = AssetManager()
    with pytest.raises(FileNotFoundError):
        assets.get_image("assets/non_existent_image.png")


def test_asset_manager_caches_font():
    assets = AssetManager()
    font1 = assets.get_font("assets/DigitalDisco-Thin.ttf", 24)
    font2 = assets.get_font("assets/DigitalDisco-Thin.ttf", 24)

    assert font1 is font2


def test_asset_manager_loads_structured_dictionaries():
    assets = AssetManager()
    tower_images = assets.get_tower_images()
    assert "basic" in tower_images
    assert "sniper" in tower_images
    assert "cannon" in tower_images
    assert "freeze" in tower_images

    enemy_images = assets.get_enemy_images()
    assert "regular" in enemy_images
    assert "fast" in enemy_images
    assert "strong" in enemy_images
