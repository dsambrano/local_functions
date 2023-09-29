import json
from typing import Dict
from notipy import notifiers
from pathlib import Path

LOCATIONS = [
    Path("notipy_config.json"),
    Path("config.json"),
    Path.home().joinpath(".config", "notipy_config.json"),
]
config_file = None
for location in LOCATIONS:
    if location.exists():
        config_file = location
        break

if config_file is None:
    print("No config files exists")
    exit()

# Read the configuration file
with config_file.open("r") as f:
    config_data = json.load(f)


def get_notifiers(config_data) -> list[notifiers.Notifier]:
    # Extract the preferred notification methods as a list
    preferred_methods = config_data.get("notification_methods", [])
    # Create a list of notification objects based on the user's choices
    notipyers = []
    for method in preferred_methods:
        try:
            notipyers.append(notifiers.create_notifier(method))
        except ValueError as e:
            print(e)
    return notipyers


def send_notifications(
    message: str, notifiers: list[notifiers.Notifier], config_data: Dict
):
    print(config_data)
    # Notify the user using all selected notification methods
    for notifier in notifiers:
        notifier.notify(message)


def main(config_data):
    notifiers = get_notifiers(config_data)
    message = "Here is a test notification to ensure everything is set up correctly"
    send_notifications(message, notifiers, config_data)


if __name__ == "__main__":
    main(config_data)
