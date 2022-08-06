import pathlib

DATA_DIRECTORY = pathlib.Path.home() / "data"
LOG_FILE_PATH = DATA_DIRECTORY / "log.txt" 
ACTIONS_DIRECTORY = DATA_DIRECTORY / "actions"

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
        self.position_x = parts[0]
        self.position_y = parts[1]
        self.position_z = parts[2]

class Action:
    def __init__(self, action_dir):
        self.action_filepath = action_dir / "action"
        with open(self.action_filepath, "r") as action_file:
            self.actions = action_file.readlines()
            self.actions = [action.strip() for action in self.actions]

# Read log file
logs = list()
with open(LOG_FILE_PATH, "r") as log_file:
    logs = log_file.readlines()
logs = [CraftLog(log_str) for log_str in logs]

# Read action files
action_dirs = ACTIONS_DIRECTORY.iterdir()
actions = [Action(action_dir) for action_dir in action_dirs]