TOWER_DATA = {
    "basic": [
        {
            "damage": 7.5,
            "range": 2,
            "atk_speed": 1.25,
            "rotate_speed": 90,
            "cost": 20,
            "sell": 43
        },
        {
            "damage": 9.4,
            "range": 2.2,
            "atk_speed": 1.4,
            "rotate_speed": 90,
            "cost": 26,
            "sell": 61
        },
        {
            "damage": 11.8,
            "range": 2.3,
            "atk_speed": 1.4,
            "rotate_speed": 110,
            "cost": 42,
            "sell": 85
        },
        {
            "damage": 14.5,
            "range": 2.3,
            "atk_speed": 1.55,
            "rotate_speed": 120,
            "cost": 61,
            "sell": 122
        },
        {
            "damage": 18,
            "range": 2.5,
            "atk_speed": 1.55,
            "rotate_speed": 120,
            "cost": 90,
            "sell": 177
        },
        {
            "damage": 23,
            "range": 2.5,
            "atk_speed": 1.7,
            "rotate_speed": 135,
            "cost": -1,
            "sell": 258
        }
    ],
    "sniper": [
        {
            "damage": 46,
            "range": 4.5,
            "atk_speed": 0.28,
            "rotate_speed": 50,
            "cost": 42,
            "sell": 72
        },
        {
            "damage": 64,
            "range": 4.9,
            "atk_speed": 0.32,
            "rotate_speed": 55,
            "cost": 72,
            "sell": 110
        },
        {
            "damage": 84,
            "range": 5.3,
            "atk_speed": 0.38,
            "rotate_speed": 60,
            "cost": 110,
            "sell": 175
        },
        {
            "damage": 128,
            "range": 5.3,
            "atk_speed": 0.38,
            "rotate_speed": 64,
            "cost": 176,
            "sell": 274
        },
        {
            "damage": 180,
            "range": 5.7,
            "atk_speed": 0.44,
            "rotate_speed": 73,
            "cost": 380,
            "sell": 432
        },
        {
            "damage": 250,
            "range": 6.1,
            "atk_speed": 0.5,
            "rotate_speed": 73,
            "cost": -1,
            "sell": 774
        }
    ],
    "cannon": [
        {
            "damage": 14,
            "range": 1.7,
            "atk_speed": 0.6,
            "rotate_speed": 40,
            "cost": 42,
            "sell": 54
        },
        {
            "damage": 22.7,
            "range": 1.9,
            "atk_speed": 0.7,
            "rotate_speed": 50,
            "cost": 63,
            "sell": 92
        },
        {
            "damage": 30.2,
            "range": 2,
            "atk_speed": 0.7,
            "rotate_speed": 60,
            "cost": 115,
            "sell": 149
        },
        {
            "damage": 39.8,
            "range": 2.15,
            "atk_speed": 0.85,
            "rotate_speed": 70,
            "cost": 210,
            "sell": 252
        },
        {
            "damage": 52.9,
            "range": 2.15,
            "atk_speed": 1,
            "rotate_speed": 80,
            "cost": 300,
            "sell": 441
        },
        {
            "damage": 68,
            "range": 2.3,
            "atk_speed": 1.1,
            "rotate_speed": 80,
            "cost": -1,
            "sell": 711
        }
    ],
    "freeze": [
        {
            "slow_rate": 0.15,
            "range": 2,
            "cost": 42,
            "sell": 72
        },
        {
            "slow_rate": 0.20,
            "range": 2.125,
            "cost": 70,
            "sell": 110
        },
        {
            "slow_rate": 0.25,
            "range": 2.25,
            "cost": 110,
            "sell": 173
        },
        {
            "slow_rate": 0.30,
            "range": 2.4,
            "cost": 170,
            "sell": 272
        },
        {
            "slow_rate": 0.35,
            "range": 2.4,
            "cost": 270,
            "sell": 425
        },
        {
            "slow_rate": 0.40,
            "range": 2.55,
            "cost": -1,
            "sell": 668
        }
    ]
}

TOWER_TYPE_DATA = {
    "basic": {"cost": 48},
    "sniper": {"cost": 80},
    "cannon": {"cost": 60},
    "freeze": {"cost": 80}
}

TOWER_EFFECTIVENESS = {
    "basic": {
        "regular": 1.5,
        "fast": 1,
        "strong": 0.5
    },
    "sniper": {
        "regular": 1,
        "fast": 0.25,
        "strong": 1.5
    },
    "cannon": {
        "regular": 1,
        "fast": 1.5,
        "strong": 0.25
    },
}

TOWER_NAME = ["basic", "sniper", "cannon", "freeze"]
