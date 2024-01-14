import asyncio
import unittest

from exceptions.player_music_exceptions.UrlInvalidFormatYoutubeException import UrlInvalidFormatYoutubeException
from services.player_music.YoutubeDownloader import YoutubeDownloader


class YoutubeDownloaderTest(unittest.IsolatedAsyncioTestCase):

    async def test_add_music_solo_on_queue(self):
        mock_path = "/test"
        mock_url_youtube = "https://www.youtube.com/watch?v=K9mzg8ueiYA"
        youtube_downloader = YoutubeDownloader(mock_path, mock_url_youtube)
        await youtube_downloader.add_music_queue_to_download()
        self.assertEqual(1, youtube_downloader.get_quantity_musics_on_queue())
        self.assertEqual("NO_STATUS", youtube_downloader.get_status_download())

    async def test_add_playlist_urls_on_queue(self):
        mock_path = "/test"
        mock_url_youtube_playlist = "https://www.youtube.com/playlist?list=PLPzULCdMTsR-ARB4c5e08PioFwks16APQ"
        youtube_downloader = YoutubeDownloader(mock_path, mock_url_youtube_playlist)
        await youtube_downloader.add_music_queue_to_download()
        self.assertEqual(36, youtube_downloader.get_quantity_musics_on_queue())
        self.assertEqual("NO_STATUS", youtube_downloader.get_status_download())

    async def test_download_music(self):
        mock_path = "https://www.youtube.com/watch?v=y-wl8JZgq-8&list=PLPzULCdMTsR-ARB4c5e08PioFwks16APQ&index=4&pp=gAQBiAQB8AUB"
        mock_url_youtube = "https://www.youtube.com/watch?v=wz7dSGjiSgY&list=PLPzULCdMTsR-ARB4c5e08PioFwks16APQ&index=1&pp=gAQBiAQB8AUB"
        youtube_downloader = YoutubeDownloader(mock_path, mock_url_youtube)
        await youtube_downloader.add_music_queue_to_download()
        await youtube_downloader.download_musics_on_queue()
        self.assertEqual("FINISH", youtube_downloader.get_status_download())
        self.assertEqual(1, youtube_downloader.get_quantity_files_downloaded())

    async def test_download_playlist_music(self):
        mock_path = "C:\\Users\\didvg\\Desktop\\DevFolders\\MelLover2.0folder_for_downloads_musics"
        mock_url_youtube = "https://www.youtube.com/playlist?list=PLPzULCdMTsR8c0kxqTBXnKdqnI7RdJ2vo"
        youtube_downloader = YoutubeDownloader(mock_path, mock_url_youtube)
        await youtube_downloader.add_music_queue_to_download()
        await youtube_downloader.download_musics_on_queue()
        self.assertEqual("FINISH", youtube_downloader.get_status_download())
        self.assertEqual(2, youtube_downloader.get_quantity_files_downloaded())

    async def test_check_if_file_already_downloaded(self):
        mock_path = "C:\\Users\\didvg\\Desktop\\DevFolders\\MelLover2.0folder_for_downloads_musics"
        mock_url_youtube = "https://www.youtube.com/watch?v=wz7dSGjiSgY&list=PLPzULCdMTsR-ARB4c5e08PioFwks16APQ&index=1&pp=gAQBiAQB8AUB"
        youtube_downloader = YoutubeDownloader(mock_path, mock_url_youtube)
        await youtube_downloader.add_music_queue_to_download()
        await youtube_downloader.download_musics_on_queue()
        self.assertEqual("SKIPPED", youtube_downloader.get_status_download())
        self.assertEqual(0, youtube_downloader.get_quantity_files_downloaded())

    def test_invalid_url_format_youtube(self):
        mock_path = "/test"
        mock_url = "failurl.com"
        with self.assertRaises(UrlInvalidFormatYoutubeException) as context:
            YoutubeDownloader(mock_path, mock_url)
        self.assertEqual("The url must be from YouTube", context.exception.__str__())


if __name__ == '__main__':
    unittest.main()
