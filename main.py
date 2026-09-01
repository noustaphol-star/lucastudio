import sys
import json
import os
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow


def resource_path(relative_path):
    """Resolve resource paths for both dev and PyInstaller-bundled runs."""
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


def load_config():
    with open(resource_path("config.json"), "r") as f:
        return json.load(f)


def main():
    config = load_config()
    app = QApplication(sys.argv)
    window = MainWindow(config)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
