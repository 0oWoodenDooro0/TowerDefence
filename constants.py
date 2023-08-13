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
            "cost": 750,
            "description": "+5"
        },
        {
            "bonus": 5,
            "cost": 800,
            "description": "+10"
        },
        {
            "bonus": 15,
            "cost": 950,
            "description": "+15"
        },
        {
            "bonus": 30,
            "cost": 1050,
            "description": "+20"
        },
        {
            "bonus": 50,
            "cost": 1200,
            "description": "+25"
        },
        {
            "bonus": 75,
            "cost": -1,
            "description": "MAX"
        }
    ],
    "starting_health_bonus": [
        {
            "bonus": 0,
            "cost": 800,
            "description": "+1"
        },
        {
            "bonus": 1,
            "cost": 1900,
            "description": "+3"
        },
        {
            "bonus": 4,
            "cost": 1800,
            "description": "+5"
        },
        {
            "bonus": 9,
            "cost": 2400,
            "description": "+7"
        },
        {
            "bonus": 16,
            "cost": 4500,
            "description": "+9"
        },
        {
            "bonus": 25,
            "cost": -1,
            "description": "MAX"
        }
    ],
    "rotate_speed": [
        {
            "bonus": 1,
            "cost": 1100,
            "description": "+1%"
        },
        {
            "bonus": 1.01,
            "cost": 1800,
            "description": "+2%"
        },
        {
            "bonus": 1.03,
            "cost": 2000,
            "description": "+3%"
        },
        {
            "bonus": 1.06,
            "cost": 3400,
            "description": "+4%"
        },
        {
            "bonus": 1.1,
            "cost": 4000,
            "description": "+5%"
        },
        {
            "bonus": 1.15,
            "cost": -1,
            "description": "MAX"
        }
    ],
    "damage": [
        {
            "bonus": 1,
            "cost": 1400,
            "description": "+2%"
        },
        {
            "bonus": 1.02,
            "cost": 1700,
            "description": "+4%"
        },
        {
            "bonus": 1.06,
            "cost": 3200,
            "description": "+6%"
        },
        {
            "bonus": 1.12,
            "cost": 3400,
            "description": "+8%"
        },
        {
            "bonus": 1.2,
            "cost": 6000,
            "description": "+11%"
        },
        {
            "bonus": 1.31,
            "cost": -1,
            "description": "MAX"
        }
    ],
    "range": [
        {
            "bonus": 1,
            "cost": 1500,
            "description": "+0.5%"
        },
        {
            "bonus": 1.005,
            "cost": 1700,
            "description": "+1%"
        },
        {
            "bonus": 1.015,
            "cost": 3600,
            "description": "+1.5%"
        },
        {
            "bonus": 1.03,
            "cost": 3600,
            "description": "+2.5%"
        },
        {
            "bonus": 1.055,
            "cost": 7000,
            "description": "+3.5%"
        },
        {
            "bonus": 1.09,
            "cost": -1,
            "description": "MAX"
        }
    ],
    "atk_speed": [
        {
            "bonus": 1,
            "cost": 1000,
            "description": "+2%"
        },
        {
            "bonus": 1.02,
            "cost": 1500,
            "description": "+4%"
        },
        {
            "bonus": 1.06,
            "cost": 2500,
            "description": "+6%"
        },
        {
            "bonus": 1.12,
            "cost": 3000,
            "description": "+9%"
        },
        {
            "bonus": 1.21,
            "cost": 4600,
            "description": "+12%"
        },
        {
            "bonus": 1.33,
            "cost": -1,
            "description": "MAX"
        }
    ],
    "sell": [
        {
            "bonus": 1,
            "cost": 800,
            "description": "+1%"
        },
        {
            "bonus": 1.01,
            "cost": 1400,
            "description": "+2%"
        },
        {
            "bonus": 1.03,
            "cost": 2200,
            "description": "+2%"
        },
        {
            "bonus": 1.05,
            "cost": 2800,
            "description": "+2%"
        },
        {
            "bonus": 1.07,
            "cost": 3200,
            "description": "+2%"
        },
        {
            "bonus": 1.09,
            "cost": -1,
            "description": "MAX"
        }
    ],
    "cost": [
        {
            "bonus": 1,
            "cost": 1000,
            "description": "-3%"
        },
        {
            "bonus": 0.97,
            "cost": 1600,
            "description": "-4%"
        },
        {
            "bonus": 0.91,
            "cost": 2000,
            "description": "-10%"
        },
        {
            "bonus": 0.81,
            "cost": 3600,
            "description": "-14%"
        },
        {
            "bonus": 0.67,
            "cost": 5500,
            "description": "-18%"
        },
        {
            "bonus": 0.49,
            "cost": -1,
            "description": "MAX"
        }
    ],
    "coin_bonus": [
        {
            "bonus": 1,
            "cost": 1000,
            "description": "+1%"
        },
        {
            "bonus": 1.01,
            "cost": 1600,
            "description": "+3%"
        },
        {
            "bonus": 1.04,
            "cost": 2000,
            "description": "+6%"
        },
        {
            "bonus": 1.1,
            "cost": 3200,
            "description": "+10%"
        },
        {
            "bonus": 1.2,
            "cost": 5000,
            "description": "+15%"
        },
        {
            "bonus": 1.35,
            "cost": -1,
            "description": "MAX"
        }
    ],
}
