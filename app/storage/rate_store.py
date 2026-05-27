import json
import os
from datetime import datetime

FILE_PATH = "app/storage/last_rates.json"


# -------------------------
# Load all history
# -------------------------
def load_data():
    if not os.path.exists(FILE_PATH):
        return {}

    with open(FILE_PATH, "r") as f:
        return json.load(f)


# -------------------------
# Save full dataset
# -------------------------
def save_data(data):
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)


# -------------------------
# Get today's data
# -------------------------
def get_today_key():
    return datetime.now().strftime("%Y-%m-%d")


# -------------------------
# Get today's rates
# -------------------------
def get_today_rates():
    data = load_data()
    today = get_today_key()
    return data.get(today)


# -------------------------
# Save today's rates
# -------------------------
def save_today_rates(new_rates):
    data = load_data()
    today = get_today_key()

    data[today] = new_rates
    save_data(data)


# -------------------------
# Change detection
# -------------------------
def has_changed(new_rates):
    today = get_today_key()
    data = load_data()

    old = data.get(today)

    if not old:
        return True  # first run today

    return old != new_rates