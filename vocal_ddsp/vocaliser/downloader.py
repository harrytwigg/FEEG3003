#!/usr/bin/env python3
import click
from pathlib import Path
from decouple import config
from typing import Union

from deezer import Deezer
from deezer import TrackFormats

from deemix import generateDownloadObject
from deemix.settings import load as loadSettings
from deemix.utils import getBitrateNumberFromText, formatListener
import deemix.utils.localpaths as localpaths
from deemix.downloader import Downloader
from deemix.itemgen import GenerationError
try:
    from deemix.plugins.spotify import Spotify
except ImportError:
    Spotify = None


class LogListener:
    @classmethod
    def send(cls, key, value=None):
        logString = formatListener(key, value)
        if logString: print(logString)


def download_raw(url, bitrate, portable, path):
        """Clone of Deemix Downloader"""

        # Check for local configFolder
        localpath = Path('.')
        configFolder = localpath / 'config' if portable else localpaths.getConfigFolder()

        settings = loadSettings(configFolder)
        dz = Deezer()
        listener = LogListener()

        def requestValidArl():
            return config('DEEZER_ARL')

        if (configFolder / '.arl').is_file():
            with open(configFolder / '.arl', 'r', encoding="utf-8") as f:
                arl = f.readline().rstrip("\n").strip()
            if not dz.login_via_arl(arl): arl = requestValidArl()
        else: arl = requestValidArl()
        with open(configFolder / '.arl', 'w', encoding="utf-8") as f:
            f.write(arl)

        plugins = {}
        if Spotify:
            plugins = {
                "spotify": Spotify(configFolder=configFolder)
            }
            plugins["spotify"].setup()

        def downloadLinks(url, bitrate=None):
            if not bitrate: bitrate = settings.get("maxBitrate", TrackFormats.MP3_320)
            links = []
            for link in url:
                if ';' in link:
                    for l in link.split(";"):
                        links.append(l)
                else:
                    links.append(link)

            downloadObjects = []

            for link in links:
                try:
                    downloadObject = generateDownloadObject(dz, link, bitrate, plugins, listener)
                except GenerationError as e:
                    print(f"{e.link}: {e.message}")
                    continue
                if isinstance(downloadObject, list):
                    downloadObjects += downloadObject
                else:
                    downloadObjects.append(downloadObject)

            for obj in downloadObjects:
                if obj.__type__ == "Convertable":
                    obj = plugins[obj.plugin].convert(dz, obj, settings, listener)
                Downloader(dz, obj, settings, listener).start()


        if path is not None:
            if path == '': path = '.'
            path = Path(path)
            settings['downloadLocation'] = str(path)
        url = list(url)
        if bitrate: bitrate = getBitrateNumberFromText(bitrate)

        # If first url is filepath readfile and use them as URLs
        try:
            isfile = Path(url[0]).is_file()
        except Exception:
            isfile = False
        if isfile:
            filename = url[0]
            with open(filename, encoding="utf-8") as f:
                url = f.readlines()

        downloadLinks(url, bitrate)
        click.echo("All done!")


def download(url: Union[str, list]):
    """Downloads a Deezer link or a list of links"""

    # Cast to list if single url
    if isinstance(url, str):
        url = [url]
    
    # Set path to parent directory of current directory and then download folder
    root_path = Path('.').parent
    downloads_path = root_path.joinpath('downloads')

    # If downloads folder doesnt exist at path, create it
    if not downloads_path.exists():
        downloads_path.mkdir()

    return download_raw(url, config('DEEZER_BITRATE'), False, downloads_path)

def download_artist(name, artist_url):
    """Downloads all tracks of an artist"""

    root_path = Path('.').parent
    downloads_path = root_path.joinpath('downloads')

    # If downloads folder doesnt exist at path, create it
    if not downloads_path.exists():
        downloads_path.mkdir()
    
    artist_path = downloads_path.joinpath(name)
    if not artist_path.exists():
        artist_path.mkdir()
    
    return download_raw([artist_url], config('DEEZER_BITRATE'), False, artist_path)


download_artist("Taylor Swift", "https://www.deezer.com/en/artist/12246")