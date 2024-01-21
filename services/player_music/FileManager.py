import os
import time

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

    async def verify_if_file_exist(self, fileName):
        full_path = os.path.join(self.path, fileName)
        return os.path.isfile(full_path)

    def get_quantity_files_music_in_folder(self):
        self.files = os.listdir(self.path)
        return len(self.files)

    def get_files_on_folder(self):
        return os.listdir(self.path)
