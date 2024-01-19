import unittest

from services.player_music.Player import Player
from constants.Contants import DEFAULT_PATH_FOLDER_DOWNLOAD


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


    def test_play(self):
        player = Player(DEFAULT_PATH_FOLDER_DOWNLOAD, "!mplay )

if __name__ == '__main__':
    unittest.main()
