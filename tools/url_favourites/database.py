from os import path
import sys
sys.path.append(path.join(path.dirname(path.abspath(__file__)), '..', '..', 'lib'))

from lib.log import get_logger
from lib.json_database import JSONDatabase
from url_favourite import URLFavourite


LOGGER = get_logger()


class URLFavouriteDatabase(JSONDatabase):

    @staticmethod
    def get_template():
        json_template = {}
        json_template['browser'] = 'firefox'
        json_template['favourites'] = []
        return json_template

    def __init__(self):
        super().__init__('url_favourites', URLFavouriteDatabase.get_template())

    def set_browser(self, browser, path):
        self.data['browser'] = browser
        if path is not None:
            LOGGER.info("Setting browser '%s' path to '%s'", browser, path)
            self.data['browser_path'] = path
        self.save()
