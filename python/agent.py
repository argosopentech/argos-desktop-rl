from utils import *
import random

import desktop_controller

d = desktop_controller.DesktopController()

while True:
    action = random.choice(
        [
            desktop_controller.InputEvent.KEY_W,
            desktop_controller.InputEvent.KEY_A,
            desktop_controller.InputEvent.KEY_S,
            desktop_controller.InputEvent.KEY_D,
            desktop_controller.InputEvent.KEY_SPACE,
        ]
    )
    d.input_event(action)
    action_str = desktop_controller.InputEvent.input_events_dict[action]
    print(action_str)
