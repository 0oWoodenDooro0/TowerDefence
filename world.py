import random

from enemy_data import ENEMY_SPAWN_DATA


class World:
    def __init__(self, map_image, data, health, money, last_enemy_spawn, spawn_cooldown):
        self.game_speed = 1
        self.run_pause = False
        self.game_pause = False
        self.game_over = False
        self.last_enemy_spawn = last_enemy_spawn - spawn_cooldown
        self.elapsed_time = 0
        self.level = 0
        self.image = map_image
        self.tower_tile_id = []
        self.tile_map = []
        self.waypoints = []
        self.level_data = data
        self.health = health
        self.money = money
        self.enemy_list = []
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0
        self.process_data()

    def process_data(self):
        for layer in self.level_data["layers"]:
            match layer["name"]:
                case "waypoints":
                    waypoints = layer["objects"][0]["polyline"]
                    self.process_waypoints(waypoints)
                case "tower":
                    self.tile_map = layer["data"]
                    tower_tile_set = set(x for x in self.tile_map if x != 0)
                    self.tower_tile_id = list(tower_tile_set)

    def process_waypoints(self, data):
        for point in data:
            x = point["x"]
            y = point["y"]
            self.waypoints.append((x, y))

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

    def restart(self, health, money, spawn_cooldown):
        self.game_speed = 1
        self.run_pause = False
        self.game_pause = False
        self.game_over = False
        self.last_enemy_spawn = self.last_enemy_spawn - spawn_cooldown
        self.elapsed_time = 0
        self.level = 0
        self.health = health
        self.money = money
        self.enemy_list = []
        self.spawned_enemies = 0
        self.killed_enemies = 0
        self.missed_enemies = 0

    def update_speed(self):
        self.game_speed = self.game_speed % 3 + 1

    def update(self):
        if self.health <= 0:
            self.game_over = True

    def pause(self, time: int):
        if self.run_pause:
            self.elapsed_time = time - self.last_enemy_spawn
        else:
            if self.game_pause:
                self.elapsed_time = time - self.last_enemy_spawn
            else:
                self.last_enemy_spawn = time - self.elapsed_time
