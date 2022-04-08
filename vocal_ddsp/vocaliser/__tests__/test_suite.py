from os import path
import unittest
from vocaliser.__tests__.downloader import TestDownloader

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestDownloader('https://deezer.page.link/86ZxcoK4eWgGCQWb7'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
