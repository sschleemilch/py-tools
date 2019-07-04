from os import path
import sys
sys.path.append(path.join(path.dirname(path.abspath(__file__)), '..', '..', 'lib'))

import webbrowser

from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

from lib.log import get_logger

LOGGER = get_logger()


class URLFavourite():

    def __init__(self, alias, url, group=None):
        self.alias = alias
        self.url = url
        if group:
            self.group = group
        else:
            self.group = "None"

    def reachable(self):
        LOGGER.debug("Checking if url '%s' is reachable", self.url)
        try:
            request = Request(self.url)
            urlopen(request, timeout=2)
            return True
        except HTTPError:
            LOGGER.warning("HTTPError occured.")
            return False
        except URLError:
            LOGGER.warning("URLError occured.")
            return False

    def open(self, browser, extend):
        try:
            webbrowser.get(browser).open_new_tab(self.url)
        except webbrowser.Error as e:
            LOGGER.error("Could not open website '%s'", e)
