import psutil


class ProcessMonitor:
    """Checks whether a target process is currently running.
    Does not read or touch any token/session files."""

    @staticmethod
    def is_running(process_name: str) -> bool:
        for proc in psutil.process_iter(['name']):
            try:
                if proc.info['name'] and process_name.lower() in proc.info['name'].lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False

    def get_status(self, targets: list) -> dict:
        return {name: self.is_running(name) for name in targets}
