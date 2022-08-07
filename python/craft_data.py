import pathlib
import math
import shutil
from collections import defaultdict

from config import *


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
logs = filter(lambda x: x.type == "on_position", logs)

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

    if current_frame.screen is None:
        continue

    if current_frame.action is None:
        continue

    previous_x = previous_frame.craft_log.position_x
    next_x = next_frame.craft_log.position_x

    loss = next_x - previous_x
    current_frame.set_loss(loss)


# Select data
frames_list = frames.items()
frames_list = filter(lambda x: x[1].loss is not None, frames_list)
frames_list_sorted = sorted(
    frames_list,
    key=lambda x: x[1].loss,
    reverse=True,
)
SELECTION_RATIO = 0.15
training_frames = frames_list_sorted[: int(len(frames_list_sorted) * SELECTION_RATIO)]

# Export training data
if TRAINING_DATA_DIRECTORY.exists():
    shutil.rmtree(TRAINING_DATA_DIRECTORY)
for timestamp, frame in training_frames:
    frame_dir = TRAINING_DATA_DIRECTORY / str(timestamp)
    frame_dir.mkdir(parents=True)

    screenshot_path = frame_dir / "screen.png"
    if frame.screen is None:
        continue
    screenshot_path.write_bytes(frame.screen.screenshot_filepath.read_bytes())

    action_path = frame_dir / "action"
    with open(action_path, "w") as action_file:
        action_file.writelines(frame.action.actions)
    print(frame.action.actions)
