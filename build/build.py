"""Run this ON WINDOWS to produce a real MyLauncher.exe.
PyInstaller cannot cross-compile, so this script must run on a Windows
machine (or a Windows CI runner, see .github/workflows/build-windows.yml).
"""
import subprocess
import shutil
import os
import platform

def build():
    if platform.system() != "Windows":
        print("⚠️  Warning: this will NOT produce a .exe on a non-Windows OS.")
        print("   Run this on Windows, or use the GitHub Actions workflow instead.")

    print("🔨 Building executable...")

    for folder in ["dist", "build_temp"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)

    result = subprocess.run([
        "pyinstaller",
        "build/build.spec",
        "--distpath", "dist",
        "--workpath", "build_temp",
        "--clean",
        "--noconfirm",
    ])

    if result.returncode == 0:
        print("✅ Build succeeded: dist/MyLauncher.exe")
    else:
        print("❌ Build failed")

if __name__ == "__main__":
    build()
