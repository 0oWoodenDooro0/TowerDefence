ROWS = 15
COLS = 15
TILE_SIZE = 64
SCREEN_WIDTH = TILE_SIZE * COLS
SCREEN_HEIGHT = TILE_SIZE * ROWS
SIDE_PANEL = 300
FPS = 60
TITLE = "Tower Defence"
MONEY = 200
HEALTH = 5
DEFAULT_DATA = {
    "coin": 0,
    "starting_money_bonus": 0,
    "starting_health_bonus": 0,
    "rotate_speed": 0,
    "damage": 0,
    "range": 0,
    "atk_speed": 0,
    "sell": 0,
    "cost": 0,
    "coin_bonus": 0
}
RESEARCH = {
    "starting_money_bonus": [
        {
            "bonus": 0,
            "cost": 750
        },
        {
            "bonus": 5,
            "cost": 800
        },
        {
            "bonus": 15,
            "cost": 950
        },
        {
            "bonus": 30,
            "cost": 1050
        },
        {
            "bonus": 50,
            "cost": 1200
        },
        {
            "bonus": 75,
            "cost": -1
        }
    ],
    "starting_health_bonus": [
        {
            "bonus": 0,
            "cost": 800
        },
        {
            "bonus": 1,
            "cost": 1900
        },
        {
            "bonus": 4,
            "cost": 1800
        },
        {
            "bonus": 9,
            "cost": 2400
        },
        {
            "bonus": 16,
            "cost": 4500
        },
        {
            "bonus": 25,
            "cost": -1
        }
    ],
    "rotate_speed": [
        {
            "bonus": 1,
            "cost": 1100
        },
        {
            "bonus": 1.01,
            "cost": 1800
        },
        {
            "bonus": 1.03,
            "cost": 2000
        },
        {
            "bonus": 1.06,
            "cost": 3400
        },
        {
            "bonus": 1.1,
            "cost": 4000
        },
        {
            "bonus": 1.15,
            "cost": -1
        }
    ],
    "damage": [
        {
            "bonus": 1,
            "cost": 1400
        },
        {
            "bonus": 1.02,
            "cost": 1700
        },
        {
            "bonus": 1.06,
            "cost": 3200
        },
        {
            "bonus": 1.12,
            "cost": 3400
        },
        {
            "bonus": 1.2,
            "cost": 6000
        },
        {
            "bonus": 1.31,
            "cost": -1
        }
    ],
    "range": [
        {
            "bonus": 1,
            "cost": 1500
        },
        {
            "bonus": 1.005,
            "cost": 1700
        },
        {
            "bonus": 1.015,
            "cost": 3600
        },
        {
            "bonus": 1.03,
            "cost": 3600
        },
        {
            "bonus": 1.055,
            "cost": 7000
        },
        {
            "bonus": 1.09,
            "cost": -1
        }
    ],
    "atk_speed": [
        {
            "bonus": 1.02,
            "cost": 1000
        },
        {
            "bonus": 1,
            "cost": 1500
        },
        {
            "bonus": 1.06,
            "cost": 2500
        },
        {
            "bonus": 1.12,
            "cost": 3000
        },
        {
            "bonus": 1.21,
            "cost": 4600
        },
        {
            "bonus": 1.33,
            "cost": -1
        }
    ],
    "sell": [
        {
            "bonus": 1,
            "cost": 800
        },
        {
            "bonus": 1.01,
            "cost": 1400
        },
        {
            "bonus": 1.03,
            "cost": 1900
        },
        {
            "bonus": 1.06,
            "cost": 2400
        },
        {
            "bonus": 1.1,
            "cost": 4400
        },
        {
            "bonus": 1.15,
            "cost": -1
        }
    ],
    "cost": [
        {
            "bonus": 1,
            "cost": 1000
        },
        {
            "bonus": 0.97,
            "cost": 1600
        },
        {
            "bonus": 0.91,
            "cost": 2000
        },
        {
            "bonus": 0.81,
            "cost": 3600
        },
        {
            "bonus": 0.67,
            "cost": 5500
        },
        {
            "bonus": 0.49,
            "cost": -1
        }
    ],
    "coin_bonus": [
        {
            "bonus": 1,
            "cost": 1000
        },
        {
            "bonus": 1.01,
            "cost": 1600
        },
        {
            "bonus": 1.04,
            "cost": 2000
        },
        {
            "bonus": 1.1,
            "cost": 3200
        },
        {
            "bonus": 1.2,
            "cost": 5000
        },
        {
            "bonus": 1.35,
            "cost": -1
        }
    ],
}
