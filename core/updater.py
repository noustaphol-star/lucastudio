import requests
from packaging import version


class Updater:
    def __init__(self, repo: str, current_version: str):
        self.repo = repo
        self.current_version = current_version
        self.api_url = f"https://api.github.com/repos/{repo}/releases/latest"

    def check_update(self):
        try:
            resp = requests.get(self.api_url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            latest = data["tag_name"].lstrip("v")

            if version.parse(latest) > version.parse(self.current_version):
                assets = data.get("assets", [])
                download_url = assets[0]["browser_download_url"] if assets else None
                return {
                    "version": latest,
                    "download_url": download_url,
                    "notes": data.get("body", ""),
                }
        except Exception:
            return None
        return None

    def download_update(self, url: str, dest_path: str, progress_callback=None):
        resp = requests.get(url, stream=True, timeout=30)
        total = int(resp.headers.get("content-length", 0))
        downloaded = 0
        with open(dest_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                if progress_callback:
                    progress_callback(downloaded, total)
