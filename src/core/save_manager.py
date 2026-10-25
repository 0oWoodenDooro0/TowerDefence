import json
import os
from src.data.constants import DEFAULT_DATA
from src.core.bonus import Bonus


class SaveManager:
    """Handles persistence of player progression (Coin and Research levels)."""

    def __init__(self, filepath: str = "assets/data.json"):
        self.filepath = filepath

    def load_data(self) -> dict:
        """Loads progression data, falling back to DEFAULT_DATA if file is missing or invalid."""
        if not os.path.exists(self.filepath):
            return self.reset_to_default()

        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Ensure all default keys exist
                updated = False
                for key, default_val in DEFAULT_DATA.items():
                    if key not in data:
                        data[key] = default_val
                        updated = True
                if updated:
                    self.save_data(data)
                return data
        except (json.JSONDecodeError, EnvironmentError):
            return self.reset_to_default()

    def save_data(self, data: dict) -> None:
        """Saves progression data atomically to disk to prevent corrupted writes."""
        dir_name = os.path.dirname(os.path.abspath(self.filepath))
        os.makedirs(dir_name, exist_ok=True)
        temp_filepath = f"{self.filepath}.tmp"
        with open(temp_filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        os.replace(temp_filepath, self.filepath)

    def reset_to_default(self) -> dict:
        """Resets saved data to default values and persists to disk."""
        default_copy = DEFAULT_DATA.copy()
        self.save_data(default_copy)
        return default_copy

    def add_coin_reward(self, reward: int) -> dict:
        """Adds coin reward earned from battles and saves to disk."""
        data = self.load_data()
        data["coin"] = data.get("coin", 0) + reward
        self.save_data(data)
        return data

    def upgrade_research(self, research_name: str, cost: int) -> bool:
        """Attempts to purchase a research upgrade with Coins."""
        data = self.load_data()
        if data.get("coin", 0) < cost:
            return False

        data["coin"] -= cost
        data[research_name] = data.get(research_name, 0) + 1
        self.save_data(data)
        return True

    def get_bonus(self) -> Bonus:
        """Returns a Bonus instance configured with the latest progression data."""
        return Bonus(self.load_data())
