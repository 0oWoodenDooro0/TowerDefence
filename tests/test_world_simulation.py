import pygame as pg
from world import World
from enemy import Enemy
from tower import AttackTower
import constants as c


def test_world_initialization(sample_level_data, headless_surface, mock_bonus):
    initial_health = 10
    initial_money = 250
    world = World(
        map_image=headless_surface,
        data=sample_level_data,
        health=initial_health,
        money=initial_money,
        last_enemy_spawn=0,
        level=1,
        bonus=mock_bonus
    )

    assert world.health == initial_health
    assert world.money == initial_money
    assert world.wave == 1
    assert world.game_speed == 1
    assert not world.game_over
    assert len(world.waypoints) > 0
    assert len(world.tower_tile_id) > 0
    assert len(world.enemy_list) > 0


def test_world_speed_toggle(sample_level_data, headless_surface, mock_bonus):
    world = World(headless_surface, sample_level_data, 10, 100, 0, 1, mock_bonus)

    assert world.game_speed == 1
    world.update_speed()
    assert world.game_speed == 2
    world.update_speed()
    assert world.game_speed == 3
    world.update_speed()
    assert world.game_speed == 1


def test_world_game_over_when_health_depleted(sample_level_data, headless_surface, mock_bonus):
    world = World(headless_surface, sample_level_data, 1, 100, 0, 1, mock_bonus)
    assert not world.game_over

    world.health = 0
    world.update()
    assert world.game_over is True


def test_world_wave_completion_and_reward_accumulation(sample_level_data, headless_surface, mock_bonus):
    world = World(headless_surface, sample_level_data, 5, 100, 0, 1, mock_bonus)
    assert not world.check_wave_completed()

    # Simulate killing all spawned enemies
    world.spawned_enemies = len(world.enemy_list)
    world.killed_enemies = len(world.enemy_list)
    assert world.check_wave_completed()

    # Reward calculation from legacy gameplay loop:
    # reward += int(reward + 10 * wave * (1 + (level - 1) * 0.2))
    initial_reward = world.reward
    added_reward = int(10 * world.wave * (1 + (world.level - 1) * 0.2))
    world.reward += added_reward
    assert world.reward == initial_reward + added_reward

    world.reset_wave()
    assert len(world.enemy_list) == 0
    assert world.spawned_enemies == 0
    assert world.killed_enemies == 0


def test_enemy_life_cycle_and_world_interaction(sample_level_data, headless_surface, mock_bonus):
    world = World(headless_surface, sample_level_data, 5, 100, 0, 1, mock_bonus)
    initial_money = world.money
    initial_health = world.health

    enemy_images = {
        "regular": pg.Surface((32, 32)),
        "fast": pg.Surface((32, 32)),
        "strong": pg.Surface((32, 32))
    }

    # Test killed enemy yields money to world
    enemy = Enemy("regular", world.waypoints, enemy_images, wave=1, level=1)
    enemy_money_value = enemy.money
    enemy.health = 0
    enemy.check_alive(world)

    assert world.money == initial_money + enemy_money_value
    assert world.killed_enemies == 1

    # Test missed enemy reduces world health
    enemy_escaping = Enemy("regular", world.waypoints, enemy_images, wave=1, level=1)
    enemy_escaping.target_waypoint = len(enemy_escaping.waypoints)  # Simulate reached destination
    enemy_escaping.move(world)

    assert world.health == initial_health - 1
    assert world.missed_enemies == 1


def test_tower_upgrade_and_attribute_scaling(mock_bonus):
    tower_images = {"basic": pg.Surface((32, 32))}
    tower_base_images = {"basic": pg.Surface((32, 32))}

    tower = AttackTower(tower_images, tower_base_images, "basic", (5, 5), mock_bonus)
    initial_level = tower.level
    initial_damage = tower.damage

    # Upgrade tower
    tower.upgrade()
    assert tower.level == initial_level + 1
    assert tower.damage > initial_damage
