from os import path
import sys
sys.path.append(path.join(path.dirname(path.dirname(path.abspath(__file__))), '..'))
from lib.log import get_logger
import datetime

LOGGER = get_logger()


class TodoItem():
    def __init__(self, content, date_due=None, date_created=None, date_done=None):
        self.content = content
        if date_created:
            self.date_created = datetime.datetime.strptime(date_created, '%Y-%m-%d').date()
            LOGGER.debug("Reading in Todo item from string")
            LOGGER.debug("Content '" + content + "'")
            LOGGER.debug("Creation date '" + str(self.date_created) + "'")
        else:
            self.date_created = datetime.date.today()
            LOGGER.debug("The creation date for a new Todo item '" + content + "' is '" + str(self.date_created) + "'")

        if date_due:
            if '+' in date_due:
                date_due = date_due.replace('+', '')
                if 'd' in date_due:
                    date_due = date_due.replace('d', '')
                    self.date_due = self.date_created + datetime.timedelta(days=int(date_due))
                if 'w' in date_due:
                    date_due = date_due.replace('w', '')
                    self.date_due = self.date_created + datetime.timedelta(days=int(date_due) * 7)
                if 'y' in date_due:
                    date_due = date_due.replace('y', '')
                    self.date_due = self.date_created + datetime.timedelta(days=int(date_due) * 365)
            else:
                self.date_due = datetime.datetime.strptime(date_due, '%Y-%m-%d').date()
            LOGGER.debug("The Todo item '" + content + "' should be done until '" + str(self.date_due) + "'")
        else:
            LOGGER.warning("Todo item '" + content + "' has no date_due date. Setting it to today in one year by default")
            self.date_due = self.date_created + datetime.timedelta(days=365)

        self.remaining_days = TodoItem.get_remaining_days(self.date_due)

        if date_done:
            self.date_done = datetime.datetime.strptime(date_done, '%Y-%m-%d').date()
        LOGGER.debug("You have '" + str(self.remaining_days) + " days' to do the task")

    def update_remaining_days(self):
        self.remaining_days = TodoItem.get_remaining_days(self.date_due)

    @staticmethod
    def get_remaining_days(end_date):
        now = datetime.date.today()
        diff = end_date - now
        return diff.days

    def __lt__(self, other):
        return self.remaining_days < other.remaining_days
