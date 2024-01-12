import os

from exceptions.player_music_exceptions.FailedToRemoveMusicFiles import FailedToRemoveMusicFiles


class FileManager:

    def __init__(self, path):
        self.path = path
        self.files = []

    def remove_files_music(self):
        try:
            print(self.path)
            self.files = os.listdir(self.path)
            for file in self.files:
                if file.endswith(".mp4"):
                    os.remove(os.path.join(self.path, file))
            return True
        except Exception as e:
            raise FailedToRemoveMusicFiles(e)

    def get_quantity_files_music_in_folder(self):
        self.files = os.listdir(self.path)
        return len(self.files)
