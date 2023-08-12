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
    "starting_coin_bonus": 0,
    "starting_health_bonus": 0,
    "rotation_speed": 0,
    "damage_boost": 0,
    "range_boost": 0,
    "atk_speed_boost": 0,
    "towers_sell_refund": 0,
    "upgrade_price": 0,
    "coin_bonus": 0
}
RESEARCH = {
    "starting_coin_bonus": [
        {
            "bonus": 5,
            "cost": 750
        },
        {
            "bonus": 15,
            "cost": 800
        },
        {
            "bonus": 30,
            "cost": 950
        },
        {
            "bonus": 50,
            "cost": 1050
        },
        {
            "bonus": 75,
            "cost": 1200
        }
    ],
    "starting_health_bonus": [
        {
            "bonus": 1,
            "cost": 800
        },
        {
            "bonus": 4,
            "cost": 1900
        },
        {
            "bonus": 9,
            "cost": 1800
        },
        {
            "bonus": 16,
            "cost": 2400
        },
        {
            "bonus": 25,
            "cost": 4500
        }
    ],
    "rotation_speed": [
        {
            "bonus": 1.01,
            "cost": 1100
        },
        {
            "bonus": 1.03,
            "cost": 1800
        },
        {
            "bonus": 1.06,
            "cost": 2000
        },
        {
            "bonus": 1.1,
            "cost": 3400
        },
        {
            "bonus": 1.15,
            "cost": 4000
        }
    ],
    "damage_boost": [
        {
            "bonus": 1.02,
            "cost": 1400
        },
        {
            "bonus": 1.06,
            "cost": 1700
        },
        {
            "bonus": 1.12,
            "cost": 3200
        },
        {
            "bonus": 1.2,
            "cost": 3400
        },
        {
            "bonus": 1.31,
            "cost": 6000
        }
    ],
    "range_boost": [
        {
            "bonus": 1.005,
            "cost": 1500
        },
        {
            "bonus": 1.015,
            "cost": 1700
        },
        {
            "bonus": 1.03,
            "cost": 3600
        },
        {
            "bonus": 1.055,
            "cost": 3600
        },
        {
            "bonus": 1.09,
            "cost": 7000
        }
    ],
    "atk_speed_boost": [
        {
            "bonus": 1.02,
            "cost": 1000
        },
        {
            "bonus": 1.06,
            "cost": 1500
        },
        {
            "bonus": 1.12,
            "cost": 2500
        },
        {
            "bonus": 1.21,
            "cost": 3000
        },
        {
            "bonus": 1.33,
            "cost": 4600
        }
    ],
    "towers_sell_refund": [
        {
            "bonus": 1.01,
            "cost": 800
        },
        {
            "bonus": 1.03,
            "cost": 1400
        },
        {
            "bonus": 1.06,
            "cost": 1900
        },
        {
            "bonus": 1.1,
            "cost": 2400
        },
        {
            "bonus": 1.15,
            "cost": 4400
        }
    ],
    "upgrade_price": [
        {
            "bonus": 0.97,
            "cost": 1000
        },
        {
            "bonus": 0.91,
            "cost": 1600
        },
        {
            "bonus": 0.81,
            "cost": 2000
        },
        {
            "bonus": 0.67,
            "cost": 3600
        },
        {
            "bonus": 0.49,
            "cost": 5500
        }
    ],
    "coin_bonus": [
        {
            "bonus": 1.01,
            "cost": 1000
        },
        {
            "bonus": 1.04,
            "cost": 1600
        },
        {
            "bonus": 1.1,
            "cost": 2000
        },
        {
            "bonus": 1.2,
            "cost": 3200
        },
        {
            "bonus": 1.35,
            "cost": 5000
        }
    ],
}
