from abc import ABC, abstractmethod


def create_notifier(preferred_method: str):
    if preferred_method == "cli":
        return CLINotifier()
    elif preferred_method == "text":
        return TextNotifier()
    elif preferred_method == "notify":
        return NotifyNotifier()
    else:
        raise ValueError(
            "Invalid notification method specified in the configuration file."
        )


class Notifier(ABC):
    @abstractmethod
    def notify(self, message):
        pass


class CLINotifier:
    def notify(self, message):
        # Implement CLI notification logic here
        print(f"{message} from CLI")
        pass


class TextNotifier:
    def notify(self, message):
        # Implement text notification logic here
        print(f"{message} from Text")
        pass


class EmailNotifier:
    def notify(self, message):
        # Implement notification logic here
        print(f"{message} from Email")
        pass


class NotifyNotifier:
    def notify(self, message):
        # Implement notification logic here
        print(f"{message} from Notify")
        pass
