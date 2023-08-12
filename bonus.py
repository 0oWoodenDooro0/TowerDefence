import constants as c


class Bonus:
    def __init__(self, bonus_data):
        self.bonus_data = bonus_data

    def get_bonus_data(self, s):
        return c.RESEARCH[s][self.bonus_data[s]]["bonus"]
