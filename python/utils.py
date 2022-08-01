import pathlib
import time

DATA_DIR = pathlib.Path.home() / "Desktop" / "desktop-rl-data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_time_str():
    return str(int(time.time()))


def get_frame_dir():
    frame_dir = DATA_DIR / get_time_str()
    frame_dir.mkdir(parents=True, exist_ok=True)
    return frame_dir
