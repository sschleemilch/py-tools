from os import path
import sys
sys.path.append(path.join(path.dirname(path.dirname(path.abspath(__file__))), '..'))
import argparse
import re

from lib.log import get_logger, add_debug_argument
from lib.print.pretty import *
from lib.print.color_string import *

from database import BirthdayDatabase

LOGGER = get_logger()
DATABASE = None


def birthday_type(input, pattern=re.compile(r"\d{4}-\d{2}-\d{2}")):
    if not pattern.match(input):
        LOGGER.error("Birthday date has to match the pattern YYYY-MM-DD")
        raise argparse.ArgumentTypeError
    return input


def get_parser():
    parser = argparse.ArgumentParser()
    parser = add_debug_argument(parser)

    subparsers = parser.add_subparsers(dest='cmd')

    parser_add = subparsers.add_parser('add', help='Add a new birthday')
    parser_add.add_argument('--first-name', '-fn', dest='first_name', required=True, help='First name of the person')
    parser_add.add_argument('--last-name', '-ln', dest='last_name', required=True, help='Last name of the person')
    parser_add.add_argument('--date', '-d', dest='birthday_date', required=True, help='Birthday date in the format YYYY-MM-DD', type=birthday_type)
    parser_add.set_defaults(func=add)

    parser_show = subparsers.add_parser('show', help='Showing birthdays')
    timespan_group = parser_show.add_mutually_exclusive_group(required=True)
    timespan_group.add_argument('--next-week', '-nw', dest='next_week', action='store_true', help='Shows upcoming birthdays the next 7 days.')
    timespan_group.add_argument('--next-days', '-nd', dest='next_days', type=int, help='Shows upcoming birthdays for the given timespan in days.')
    timespan_group.add_argument('--all', '-a', dest='all', action='store_true', help='Shows all birthdays sorted after next occurence.')

    parser_delete = subparsers.add_parser('delete', help='Deletes a birthday from database')
    parser_delete.add_argument('--first-name', '-fn', dest='first_name', required=True, help='First name of the person')
    parser_delete.add_argument('--last-name', '-ln', dest='last_name', required=True, help='Last name of the person')

    return parser


def add(args):
    DATABASE.add_birthday(args.first_name, args.last_name, args.birthday_date)


def show(args):
    if args.all:
        birthdays_to_show = DATABASE.get_all_upcoming_birthdays_sorted()
    if args.next_week:
        birthdays_to_show = DATABASE.get_upcoming_birthdays_for_next_days(7)
    if args.next_days:
        birthdays_to_show = DATABASE.get_upcoming_birthdays_for_next_days(args.next_days)

    printer = Printer(box_color=Color.grey, title_color=Color.green, content_color=Color.green)
    printer.title('BIRTHDAYS')

    for birthday in birthdays_to_show:
        content = birthday.first_name + ' ' + birthday.last_name + ' (turns ' + str(birthday.age + 1) + ')'
        printer.print(content, status=Status.ok, status_content=str(birthday.days_until_birthday))

    printer.divider()


def delete(args):
    DATABASE.delete_birthday(args.first_name, args.last_name)


def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.debug:
        LOGGER.setLevel('DEBUG')

    global DATABASE
    DATABASE = BirthdayDatabase()

    if args.cmd:
        if args.cmd == 'add':
            add(args)
        if args.cmd == 'show':
            show(args)
        if args.cmd == 'delete':
            delete(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
