TOWER_DATA = {
    "basic": [
        {
            "damage": 7.5,
            "range": 140,
            "cooldown": 800,
            "cost": 20,
            "sell": 43
        },
        {
            "damage": 9.4,
            "range": 154,
            "cooldown": 710,
            "cost": 26,
            "sell": 61
        },
        {
            "damage": 11.8,
            "range": 161,
            "cooldown": 710,
            "cost": 42,
            "sell": 85
        },
        {
            "damage": 14.5,
            "range": 161,
            "cooldown": 660,
            "cost": 61,
            "sell": 122
        },
        {
            "damage": 18,
            "range": 175,
            "cooldown": 590,
            "cost": 90,
            "sell": 177
        },
        {
            "damage": 23,
            "range": 175,
            "cooldown": 590,
            "cost": -1,
            "sell": 258
        }
    ],
    "sniper": [
        {
            "damage": 46,
            "range": 315,
            "cooldown": 3550,
            "cost": 42,
            "sell": 72
        },
        {
            "damage": 64,
            "range": 343,
            "cooldown": 3150,
            "cost": 72,
            "sell": 110
        },
        {
            "damage": 84,
            "range": 371,
            "cooldown": 2650,
            "cost": 110,
            "sell": 175
        },
        {
            "damage": 128,
            "range": 371,
            "cooldown": 2650,
            "cost": 176,
            "sell": 274
        },
        {
            "damage": 180,
            "range": 399,
            "cooldown": 2250,
            "cost": 380,
            "sell": 432
        },
        {
            "damage": 250,
            "range": 427,
            "cooldown": 2200,
            "cost": -1,
            "sell": 774
        }
    ],
    "cannon": [
        {
            "damage": 14,
            "range": 119,
            "cooldown": 1650,
            "cost": 42,
            "sell": 54
        },
        {
            "damage": 22.7,
            "range": 133,
            "cooldown": 1400,
            "cost": 63,
            "sell": 92
        },
        {
            "damage": 30.2,
            "range": 140,
            "cooldown": 1400,
            "cost": 115,
            "sell": 149
        },
        {
            "damage": 39.8,
            "range": 150,
            "cooldown": 1170,
            "cost": 210,
            "sell": 252
        },
        {
            "damage": 52.9,
            "range": 150,
            "cooldown": 1000,
            "cost": 300,
            "sell": 441
        },
        {
            "damage": 68,
            "range": 161,
            "cooldown": 900,
            "cost": -1,
            "sell": 711
        }
    ],
    "freeze": [
        {
            "slow_rate": 0.15,
            "range": 140,
            "cost": 42,
            "sell": 72
        },
        {
            "slow_rate": 0.20,
            "range": 149,
            "cost": 70,
            "sell": 110
        },
        {
            "slow_rate": 0.25,
            "range": 158,
            "cost": 110,
            "sell": 173
        },
        {
            "slow_rate": 0.30,
            "range": 168,
            "cost": 170,
            "sell": 272
        },
        {
            "slow_rate": 0.35,
            "range": 168,
            "cost": 270,
            "sell": 425
        },
        {
            "slow_rate": 0.40,
            "range": 179,
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
