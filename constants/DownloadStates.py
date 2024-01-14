from enum import Enum


class DownloadStates(Enum):
    NO_STATUS = 0
    FINISH = 1
    IN_PROGRESS = 2
    ERROR = 3
    SKIPPED = 4

    def get_status_name(self):
        return self.name
