ROWS = 15
COLS = 15
TILE_SIZE = 64
SCREEN_WIDTH = TILE_SIZE * COLS
SCREEN_HEIGHT = TILE_SIZE * ROWS
SIDE_PANEL = 300
FPS = 60
TITLE = "Tower Defence"
WAYPOINTS = [
    (832, 0),
    (832, 256),
    (640, 256),
    (640, 128),
    (64, 128),
    (64, 640),
    (256, 640),
    (256, 320),
    (448, 320),
    (448, 448),
    (896, 448),
    (896, 832),
    (704, 832),
    (704, 640),
    (448, 640),
    (448, 832),
    (-50, 832)
]
TILE_MAP = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 181, 0, 0, 0,
            0, 0, 181, 0, 0, 181, 0, 0, 181, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 181, 0, 0, 181, 0, 0, 0,
            0, 0, 181, 0, 0, 181, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 181, 0, 0, 181, 0, 0, 181, 0, 0, 0, 181, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 181, 0, 0, 181, 0, 0, 0, 181, 0, 0, 181, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
TOWER_TILE_ID = 181
MAX_LEVEL = 4
SPAWN_COOLDOWN = 300
MONEY = 50
HEALTH = 5
TOWER_COST = 20
