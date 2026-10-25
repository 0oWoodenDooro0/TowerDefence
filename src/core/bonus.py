from src.data.research_data import RESEARCH


class Bonus:
    """Manages passive bonuses derived from player research levels."""

    def __init__(self, bonus_data: dict):
        self.bonus_data = bonus_data

    def get_bonus_data(self, key: str):
        if key not in RESEARCH:
            return 1.0
        level = self.bonus_data.get(key, 0)
        return RESEARCH[key][level]["bonus"]
