from os import path
import sys
sys.path.append(path.join(path.dirname(path.abspath(__file__)), '..', '..', 'lib'))
import argparse
import re

from lib.log import get_logger, add_logging_arguments
from lib.print.pretty import *
from lib.print.color_string import *

from database import TodoDatabase
from item import TodoItem

LOGGER = get_logger()
DATABASE = None


def add(args):
    new_todo_item = TodoItem(args.content, args.date_due)
    DATABASE.add_todo_item(new_todo_item)


def get_color_and_status_from_remaining_days(remaining_days):
    if remaining_days <= 1:
        return (Color.red, Status.error)
    elif remaining_days < 7:
        return (Color.yellow, Status.warning)
    else:
        return (Color.green, Status.ok)


def show(args):
    printer = Printer(box_color=Color.grey, title_color=Color.cyan)

    if args.done:
        printer.title('TODOs DONE')
    else:
        printer.title('TODOs')
    if args.done:
        todo_items = DATABASE.get_all_todo_items_sorted(show_done=True)
    else:
        todo_items = DATABASE.get_all_todo_items_sorted()
    for i in range(0, len(todo_items)):
        if args.number_of_entries and i + 1 > args.number_of_entries:
            break
        item = todo_items[i]

        if args.done:
            color = Color.cyan
            status_content = str(item.date_created) + ', ' + str(item.date_due) + ', ' + str(item.date_done)
            status = Status.info
            printer.print(item.content, color=Color.grey, status=status, status_content=status_content)
        else:
            color, status = get_color_and_status_from_remaining_days(item.remaining_days)
            identifier = str(i) + ' - '
            status_content = str(item.remaining_days) + ' remaining days'
            printer.print(identifier + item.content, status=status, color=color, status_content=status_content)
    printer.divider()


def done(args):
    todo_items = DATABASE.get_all_todo_items_sorted()
    if args.id >= len(todo_items):
        LOGGER.error("The given id '" + str(args.id) + "' does not exist.")
        return
    LOGGER.info("Deleting todo item with id '" + str(args.id) + "'")
    DATABASE.delete_todo_item(todo_items[args.id])


def clear(args):
    DATABASE.delete()


def until_type(input, pattern=re.compile(r"(?:\+\d+(?:d|w|y)|\d{4}-\d{2}-\d{2})")):
    if not pattern.match(input):
        LOGGER.error("Due date has to match either the pattern YYYY-MM-DD or a relative timespan +N[d|w|y]")
        raise argparse.ArgumentTypeError
    return input


def get_parser():
    parser = argparse.ArgumentParser()
    add_logging_arguments(parser)

    subparsers = parser.add_subparsers(dest='cmd')

    parser_add = subparsers.add_parser('add', help='Add a todo item')
    parser_add.add_argument('--item', '-i', dest='content', required=True, help='Todo item to add')
    parser_add.add_argument('--due-date', '-d', dest='date_due', required=False, help='Due date for the item. Can be either YYYY-MM-DD or +N(d|w|y)', type=until_type)
    parser_add.set_defaults(func=add)

    parser_list = subparsers.add_parser('show', help='Shows todo items sorted to next due date')
    parser_list.add_argument('-n', dest='number_of_entries', type=int, required=False, help='Todo entries to show. Default is all.')
    parser_list.add_argument('--done', '-d', action='store_true', required=False, help='Show done todo entries.')
    parser_list.set_defaults(func=show)

    parser_done = subparsers.add_parser('done', help='Marks a todo entry as done and therefore deletes it')
    parser_done.add_argument('--id', '-i', required=True, type=int, help='The id of the item that has been finished')
    parser_done.set_defaults(func=done)

    parser_clear = subparsers.add_parser('clear', help='Clears the database and creates a new empty one')
    parser_clear.set_defaults(func=clear)

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.debug:
        LOGGER.setLevel('DEBUG')
    global DATABASE
    DATABASE = TodoDatabase()
    if args.cmd:
        if args.cmd == 'add':
            add(args)
        if args.cmd == 'show':
            show(args)
        if args.cmd == 'done':
            done(args)
        if args.cmd == 'clear':
            clear(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
