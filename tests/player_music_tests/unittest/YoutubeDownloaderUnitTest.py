import unittest
from unittest.mock import patch, MagicMock, Mock

from exceptions.player_music_exceptions.UrlInvalidFormatYoutubeException import UrlInvalidFormatYoutubeException
from services.player_music.YoutubeDownloader import YoutubeDownloader
from pytube import YouTube, Playlist


class YoutubeDownloaderUnitTest(unittest.IsolatedAsyncioTestCase):
    def test_parse_url_youtube(self):
        mock_path = "//test"
        mock_url = "https://www.youtube.com/"
        try:
            YoutubeDownloader(mock_path, mock_url)  # Method parse_url on constructor
        except UrlInvalidFormatYoutubeException as e:
            self.fail(e)

    def test_exception_parse_url(self):
        mock_path = "//test"
        mock_url = "https://www.google.com"
        with self.assertRaises(UrlInvalidFormatYoutubeException) as context:
            YoutubeDownloader(mock_path, mock_url)  # Method parse_url on constructor
        self.assertEqual(context.exception.__str__(), "The url must be from YouTube")

    async def test_add_music_solo_url_on_queue(self):
        mock_path = "//test"
        mock_url = "https://www.youtube.com/watch?v=fvZizuYGMtM"
        youtube_downloader = YoutubeDownloader(mock_path, mock_url)
        await youtube_downloader.add_music_queue_download()
        self.assertEqual(1, youtube_downloader.get_quantity_musics_on_queue())

if __name__ == '__main__':
    unittest.main()
