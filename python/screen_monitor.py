from utils import *
import desktop_controller

d = desktop_controller.DesktopController()

while True:
    d.screenshot(get_frame_dir() / f"screen.png")
