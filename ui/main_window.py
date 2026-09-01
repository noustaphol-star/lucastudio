from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
)
from PyQt6.QtCore import Qt, QTimer
from core.process_monitor import ProcessMonitor
from core.updater import Updater


class StatusCard(QFrame):
    def __init__(self, title: str, description: str):
        super().__init__()
        self.setObjectName("statusCard")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")

        desc_label = QLabel(description)
        desc_label.setObjectName("cardDesc")
        desc_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addWidget(desc_label)


class MainWindow(QMainWindow):
    def __init__(self, config: dict):
        super().__init__()
        self.config = config
        self.setWindowTitle(config.get("app_name", "MyLauncher"))
        self.resize(900, 300)

        self.process_monitor = ProcessMonitor()
        self.updater = Updater(
            config.get("update_repo", ""),
            config.get("current_version", "0.0.0"),
        )

        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        self.checking_card = StatusCard(
            "Checking Account",
            "Checking whether Discord and Steam are currently running.",
        )
        self.updater_card = StatusCard(
            "Auto Updater",
            "Checks GitHub Releases for a newer version.",
        )

        layout.addWidget(self.checking_card)
        layout.addWidget(self.updater_card)

        self._apply_styles()

        # Poll process status every 5 seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_status)
        self.timer.start(5000)
        self.refresh_status()

    def refresh_status(self):
        targets = self.config.get("check_processes", [])
        status = self.process_monitor.get_status(targets)
        lines = [f"{name}: {'Running' if running else 'Not running'}"
                 for name, running in status.items()]
        self.checking_card.layout().itemAt(1).widget().setText("\n".join(lines))

    def _apply_styles(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #14151f; }
            #statusCard {
                background-color: #1c1e2c;
                border-radius: 12px;
                border: 1px solid #2a2c3d;
            }
            #cardTitle {
                color: white;
                font-size: 16px;
                font-weight: 600;
            }
            #cardDesc {
                color: #9aa0b4;
                font-size: 12px;
                margin-top: 6px;
            }
        """)
