import random

from enemy_data import ENEMY_SPAWN_DATA


class World:
    def __init__(self, map_image, tile_map, tower_tile_id, waypoints, health, money):
        self.game_speed = 1
        self.level = 0
        self.image = map_image
        self.tile_map = tile_map
        self.tower_tile_id = tower_tile_id
        self.waypoints = waypoints
        self.health = health
        self.money = money
        self.enemy_list = []
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0

    def process_enemies(self):
        enemies = ENEMY_SPAWN_DATA[self.level]
        for enemy_type in enemies:
            enemies_to_spawn = enemies[enemy_type]
            for enemy in range(enemies_to_spawn):
                self.enemy_list.append(enemy_type)
        random.shuffle(self.enemy_list)

    def draw(self, surface):
        surface.blit(self.image, (0, 0))

    def check_level_completed(self):
        return self.killed_enemies + self.missed_enemies == len(self.enemy_list)

    def reset_level(self):
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0
        self.enemy_list = []

    def update_speed(self):
        self.game_speed = self.game_speed % 3 + 1
