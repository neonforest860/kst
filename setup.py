import sys
from cx_Freeze import setup, Executable

# Dependencies
build_exe_options = {
    "packages": ["PyQt6", "requests"],
    "excludes": [],
    "include_files": [
        ("assets", "assets"),  # Include assets directory
    ]
}

# Base for Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="KonectTrafficStudio",
    version="1.1",
    description="Konect Traffic Studio Application",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "main.py",
            base=base,
            icon="assets/icons/home.png",
            target_name="KonectTrafficStudio.exe"
        )
    ]
)