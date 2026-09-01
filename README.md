# MyLauncher

A simple, transparent Python game launcher scaffold (PyQt6) with:
- Process status check (Discord/Steam running or not — no token access)
- Auto-updater that checks GitHub Releases (no silent installs)

## Run it (any OS, for development)

```bash
pip install -r requirements.txt
python main.py
```

## Build a real Windows .exe

PyInstaller **cannot cross-compile** — a `.exe` must be built on Windows.

### Option A: Build on your own Windows machine
```bash
pip install -r requirements.txt
python build/build.py
```
Output: `dist/MyLauncher.exe`

### Option B: Let GitHub build it for you (recommended)
1. Push this project to a GitHub repo.
2. Push a tag, e.g. `git tag v1.0.0 && git push --tags`
   (or run the workflow manually from the Actions tab)
3. GitHub Actions (`.github/workflows/build-windows.yml`) builds on a
   real Windows runner and attaches `MyLauncher.exe` to the release.

## Notes on avoiding false-positive AV flags
- Consider getting a code-signing certificate before distributing widely —
  unsigned .exe files are heavily penalized by heuristic/ML AV engines.
- Avoid aggressive UPX packing (`upx=False` is already set in build.spec).
- New/rarely-downloaded executables get flagged more by ML-based engines
  regardless of actual behavior; reputation builds up over time as more
  people run a signed, unchanged binary.
