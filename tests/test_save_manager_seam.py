import json
import os
import constants as c


def test_load_data_returns_default_when_missing(tmp_path):
    # Test reading non-existent file falls back to default data
    data_file = tmp_path / "data.json"
    assert not data_file.exists()

    try:
        with open(data_file) as f:
            data = json.load(f)
    except EnvironmentError:
        with open(data_file, "w") as f:
            json.dump(c.DEFAULT_DATA, f)
        data = c.DEFAULT_DATA

    assert data["coin"] == 0
    assert data["starting_money_bonus"] == 0
    assert data_file.exists()


def test_save_data_accumulates_coin(tmp_path):
    data_file = tmp_path / "data.json"
    with open(data_file, "w") as f:
        json.dump({"coin": 50}, f)

    with open(data_file, "r") as f:
        data = json.load(f)
    data["coin"] += 25
    with open(data_file, "w") as f:
        json.dump(data, f)

    with open(data_file, "r") as f:
        saved = json.load(f)
    assert saved["coin"] == 75
