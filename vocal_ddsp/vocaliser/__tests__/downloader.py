import unittest
from vocaliser.downloader import download

class TestDownloader(unittest.TestCase):
    def setUp(self):
        download("https://deezer.page.link/86ZxcoK4eWgGCQWb7")
    