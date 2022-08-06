import pathlib
from collections import defaultdict

DATA_DIRECTORY = pathlib.Path.home() / "data"
LOG_FILE_PATH = DATA_DIRECTORY / "log.txt"
ACTIONS_DIRECTORY = DATA_DIRECTORY / "actions"
SCREENSHOTS_DIRECTORY = DATA_DIRECTORY / "screenshots"


class CraftLog:
    def __init__(self, log_str):
        parts = log_str.split("    ")
        self.parse_timestamp(parts[0])
        self.type = parts[1]
        if self.type == "on_position":
            self.parse_on_position(parts[2:])

    def parse_timestamp(self, timestamp_str):
        self.timestamp = int(timestamp_str[1:-1])

    def parse_on_position(self, parts):
        self.position_x = float(parts[0])
        self.position_y = float(parts[1])
        self.position_z = float(parts[2])


class Action:
    def __init__(self, action_dir):
        self.timestamp = int(action_dir.name)
        self.action_filepath = action_dir / "action"
        with open(self.action_filepath, "r") as action_file:
            self.actions = action_file.readlines()
            self.actions = [action.strip() for action in self.actions]


class Screen:
    def __init__(self, screenshot_dir):
        self.timestamp = int(screenshot_dir.name)
        self.screenshot_filepath = screenshot_dir / "screen.png"


class Frame:
    def __init__(self):
        self.craft_log = None
        self.action = None
        self.screen = None
        self.loss = None

    def set_craft_log(self, craft_log):
        self.craft_log = craft_log

    def set_action(self, action):
        self.action = action

    def set_screen(self, screen):
        self.screen = screen

    def set_loss(self, loss):
        self.loss = loss


# Read log file
logs = list()
with open(LOG_FILE_PATH, "r") as log_file:
    logs = log_file.readlines()
logs = [CraftLog(log_str) for log_str in logs]

# Read action files
action_dirs = ACTIONS_DIRECTORY.iterdir()
actions = [Action(action_dir) for action_dir in action_dirs]

# Read screens
screenshot_dirs = SCREENSHOTS_DIRECTORY.iterdir()
screens = [Screen(screenshot_dir) for screenshot_dir in screenshot_dirs]

# Build frames map
frames = defaultdict(Frame)
for log in logs:
    frames[log.timestamp].set_craft_log(log)
for action in actions:
    frames[action.timestamp].set_action(action)
for screen in screens:
    frames[screen.timestamp].set_screen(screen)

# Compute loss
timestamps = list(frames.keys())
for timestamp in timestamps:
    previous_frame = frames[timestamp - 1]
    current_frame = frames[timestamp]
    next_frame = frames[timestamp + 1]

    if previous_frame.craft_log is None or next_frame.craft_log is None:
        continue

    previous_x = previous_frame.craft_log.position_x
    next_x = next_frame.craft_log.position_x

    loss = next_x - previous_x
    current_frame.set_loss(loss)
