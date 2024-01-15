from enum import Enum


class PlayerMusicStatus(Enum):
    SILENCE = 0
    PLAYING = 1
    SKIPPED = 2
    PAUSE = 3

    def get_status_name(self):
        return self.name
