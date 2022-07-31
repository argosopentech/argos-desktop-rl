import ctypes

desktop_controller = ctypes.CDLL("build/desktop_controller.so")

desktop_controller.key_press.argtypes = [ctypes.c_int]

print(desktop_controller.key_press(42))
