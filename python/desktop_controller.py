import ctypes
import time
import subprocess
import pathlib


class InputEvent:
    # https://github.com/torvalds/linux/blob/master/include/uapi/linux/input-event-codes.h

    InputEventCode = int

    KEY_W: InputEventCode = 17
    KEY_A: InputEventCode = 30
    KEY_S: InputEventCode = 31
    KEY_D: InputEventCode = 32
    KEY_SPACE: InputEventCode = 57

    input_events_dict = {
        KEY_W: "KEY_W",
        KEY_A: "KEY_A",
        KEY_S: "KEY_S",
        KEY_D: "KEY_D",
        KEY_SPACE: "KEY_SPACE",
    }


class DesktopController:
    def __init__(self):
        self.desktop_controller = ctypes.CDLL("build/desktop_controller.so")

        self.desktop_controller.desktop_controller_init.restype = ctypes.c_void_p
        self.desktop_controller.desktop_controller_free.argtypes = [ctypes.c_void_p]
        self.desktop_controller.input_event.argtypes = [ctypes.c_void_p, ctypes.c_int]

        self.c_desktop_controller_ptr = (
            self.desktop_controller.desktop_controller_init()
        )
        time.sleep(1)  # Give userspace time to start listening to events

    def __del__(self):
        self.desktop_controller.desktop_controller_free(self.c_desktop_controller_ptr)

    def input_event(self, event: InputEvent.InputEventCode):
        """Requires root user"""
        self.desktop_controller.input_event(self.c_desktop_controller_ptr, event)

    def screenshot(self, filepath: pathlib.Path):
        process = subprocess.run(["gnome-screenshot", "-f", str(filepath)])


# d = DesktopController()

# KEY_SPACE event
# Requires root user
# d.input_event(InputEvent.KEY_SPACE)

# Take screenshot
# d.screenshot(pathlib.Path("Screenshot.png"))
