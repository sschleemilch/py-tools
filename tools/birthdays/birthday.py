from os import path
import sys
sys.path.append(path.join(path.dirname(path.abspath(__file__)), '..', '..', 'lib'))
from lib.log import get_logger
import datetime

LOGGER = get_logger()


class Birthday():
    def __init__(self, first_name, last_name, date):
        LOGGER.debug("Birthday of '" + first_name + " " + last_name + "' is '" + date + "'")
        self.date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        self.first_name = first_name
        self.last_name = last_name

        today = datetime.date.today()
        self.age = int((today - self.date).days / 365.25)
        birthday_this_year = self.date.replace(year=today.year)
        self.days_until_birthday = (birthday_this_year - today).days

    def is_today(self):
        if self.days_until_birthday == 0:
            LOGGER.debug("Birthday of '" + self.first_name + " " + self.last_name + "' is today")
            return True
        return False

    def __lt__(self, other):
        return self.days_until_birthday < other.days_until_birthday
