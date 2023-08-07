import random

from enemy_data import ENEMY_SPAWN_DATA


class World:
    def __init__(self, map_image, tile_map, tower_tile_id, waypoints, health, money, last_enemy_spawn):
        self.game_speed = 1
        self.game_pause = False
        self.game_over = False
        self.last_enemy_spawn = last_enemy_spawn
        self.elapsed_time = 0
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

    def update(self):
        if self.health <= 0:
            self.game_over = True

    def pause(self, time: int):
        self.game_pause = not self.game_pause
        if self.game_pause:
            self.elapsed_time = time - self.last_enemy_spawn
        else:
            self.last_enemy_spawn = time - self.elapsed_time
