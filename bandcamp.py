import json
import logging

import requests
from bs4 import BeautifulSoup
from bs4 import FeatureNotFound

from bandcampjson import BandcampJSON

# modified (with thanks) from https://github.com/iheanyi/bandcamp-dl


class Bandcamp:
    def parse(self, url: str, debugging: bool=False) -> dict or None:
        """Requests the page, cherry picks album info
        :param url: album/track url
        :param debugging: if True then verbose output
        :return: album metadata
        """
        if debugging:
            logging.basicConfig(level=logging.DEBUG)
        try:
            response = requests.get(url)
        except requests.exceptions.MissingSchema:
            return None

        try:
            self.soup = BeautifulSoup(response.text, "lxml")
        except FeatureNotFound:
            self.soup = BeautifulSoup(response.text, "html.parser")

        bandcamp_json = BandcampJSON(self.soup, debugging).generate()
        page_json = {}
        for entry in bandcamp_json:
            page_json = {**page_json, **json.loads(entry)}

        first_song = page_json['trackinfo'][0]['title']

        album = {
            "title": first_song,
            "artist": page_json['artist'],
        }

        logging.debug(f" found first track {first_song} by {page_json['artist']}")
        return album
