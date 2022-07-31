import ctypes
import time

InputEventCode = int

class InputEventCodes:
    KEY_SPACE = 57

class DesktopController:
    def __init__(self):
        self.desktop_controller = ctypes.CDLL("build/desktop_controller.so")

        self.desktop_controller.desktop_controller_init.restype = ctypes.c_void_p
        self.desktop_controller.desktop_controller_free.argtypes = [ctypes.c_void_p]
        self.desktop_controller.input_event.argtypes = [ctypes.c_void_p, ctypes.c_int]

        self.c_desktop_controller_ptr = self.desktop_controller.desktop_controller_init()
        time.sleep(1) # Give userspace time to start listening to events


    def __del__(self):
        self.desktop_controller.desktop_controller_free(self.c_desktop_controller_ptr)

    def input_event(self, event : InputEventCode):
        self.desktop_controller.input_event(self.c_desktop_controller_ptr, event)

desktop_controller = DesktopController()

desktop_controller.input_event(InputEventCodes.KEY_SPACE)
