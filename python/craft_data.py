import pathlib

DATA_DIRECTORY = pathlib.Path.home() / "data"
LOG_FILE_PATH = DATA_DIRECTORY / "log.txt" 

logs = list()

with open(LOG_FILE_PATH, "r") as log_file:
    logs = log_file.readlines()

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
