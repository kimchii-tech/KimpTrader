from cx_Freeze import setup, Executable
import sys

build_exe_options = {
    "packages": ["tkinter", "json", "requests", "telegram", "pygame"],
    "include_files": [
        ("settings.json", "settings.json"),
        ("assets/alert.wav", "assets/alert.wav"),
        ("assets/icon.ico", "assets/icon.ico")
    ],
    "excludes": []
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="김프트레이더Pro",
    version="1.0",
    description="김치프리미엄 모니터링 프로그램",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "src/main.py",
            base=base,
            icon="assets/icon.ico",
            target_name="KimpTrader.exe"
        )
    ]
)