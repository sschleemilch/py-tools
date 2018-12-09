from os import path
import sys
sys.path.append(path.join(path.dirname(path.dirname(path.abspath(__file__))), '..'))

from lib.log import get_logger
from lib.json_database import JSONDatabase
from birthday import Birthday

LOGGER = get_logger()


class BirthdayDatabase(JSONDatabase):

    @staticmethod
    def get_template():
        json_database_template = {}
        json_database_template['birthdays'] = []
        return json_database_template

    def __init__(self):
        super().__init__('birthdays', BirthdayDatabase.get_template())
        LOGGER.debug("Birthday database contains '" + str(len(self.data['birthdays'])) + "' birthdays.")

    def add_birthday(self, first_name, last_name, date):
        if self.already_existing(first_name, last_name):
            LOGGER.info("Birthday of '" + first_name + " " + last_name + "' already tracked.")
        else:
            LOGGER.info("Adding new birthday of '" + first_name + " " + last_name + "'")
            new_birthday = {}
            new_birthday['first_name'] = first_name
            new_birthday['last_name'] = last_name
            new_birthday['date'] = date
            self.data['birthdays'].append(new_birthday)
            self.save()

    def already_existing(self, first_name, last_name):
        for birthday in self.data['birthdays']:
            if first_name == birthday['first_name']:
                if last_name == birthday['last_name']:
                    LOGGER.info("Birthday of '" + first_name + " " + last_name + "' already existing.")
                    return True
        LOGGER.info("Birthday of '" + first_name + " " + last_name + "' does not exist yet.")
        return False

    def get_all_upcoming_birthdays_sorted(self):
        all_birthdays = []
        for birthday in self.data['birthdays']:
            birthday_entry = Birthday(birthday['first_name'], birthday['last_name'], birthday['date'])
            if birthday_entry.days_until_birthday >= 0:
                all_birthdays.append(birthday_entry)
        all_birthdays.sort()
        return all_birthdays

    def get_upcoming_birthdays_for_next_days(self, days):
        next_birthdays = []
        all_birthdays = self.get_all_upcoming_birthdays_sorted()
        for birthday in all_birthdays:
            if birthday.days_until_birthday <= days and birthday.days_until_birthday >= 0:
                next_birthdays.append(birthday)
            else:
                break
        return next_birthdays

    def delete_birthday(self, first_name, last_name):
        if self.already_existing(first_name, last_name):
            LOGGER.info("Deleting birthday entry of '" + first_name + " " + last_name + "'.")
            for birthday in self.data['birthdays']:
                if first_name == birthday['first_name']:
                    if last_name == birthday['last_name']:
                        self.data['birthdays'].remove(birthday)
                        self.save()
        else:
            LOGGER.info("Birthday of '" + first_name + " " + last_name + "' does not exist. Nothing to delete.")
