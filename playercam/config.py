"""Where SCC Player Cam keeps its files.

The app's own pages ship inside it (unpacked by PyInstaller in the .exe);
what it writes (the window's saved settings in webview/, updates in
_update/) lives next to PlayerCam.exe, or next to the project from source.
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FROZEN = getattr(sys, "frozen", False)
RESOURCE_DIR = getattr(sys, "_MEIPASS", ROOT) if FROZEN else ROOT
DATA_DIR = os.path.dirname(os.path.abspath(sys.executable)) if FROZEN else ROOT
WEB_DIR = os.path.join(RESOURCE_DIR, "web")


def web_file(rel):
    """Path on disk for a URL path like "assets/x.png", or None (paths that try to climb out are refused)."""
    rel = rel.replace("\\", "/").lstrip("/")
    path = os.path.normpath(os.path.join(WEB_DIR, rel))
    if path.startswith(os.path.normpath(WEB_DIR) + os.sep) and os.path.isfile(path):
        return path
    return None
