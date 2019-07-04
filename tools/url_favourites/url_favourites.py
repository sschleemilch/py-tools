from os import path
import sys
sys.path.append(path.join(path.dirname(path.abspath(__file__)), '..', '..', 'lib'))

from lib.print.pretty import *
from lib.print.color_string import Color
from lib.log import get_logger, add_logging_arguments

from database import URLFavouriteDatabase

import argparse
import webbrowser


LOGGER = get_logger()
DATABASE = None


def parse_args():
    parser = argparse.ArgumentParser('FAV')
    add_logging_arguments(parser)

    subparsers = parser.add_subparsers(help='sub-commands help', dest='cmd')

    parser_config = subparsers.add_parser('config', help='Configuration options')
    parser_config.add_argument('--browser', '-b', required=True, help="Change browser ('firefox' | 'chrome')")
    parser_config.add_argument('--path', '-p', required=False, help="Specify path to browser")

    parser_add = subparsers.add_parser('add', help='Add a favourite site')
    parser_add.add_argument('--url', '-u', required=True, help='URL to add')
    parser_add.add_argument('--group', '-g', required=True, help='Group to add the URL to')
    parser_add.add_argument('--alias', '-a', required=True, help='Alias for the URL')

    parser_del = subparsers.add_parser('del', help='Delete favourite sites or groups')
    parser_del.add_argument('--group', '-g', required=False, help='Specify the group to remove')
    parser_del.add_argument('--alias', '-a', required=False, help='Specify the URL alias to remove')
    parser_del.add_argument('--url', '-u', required=False, help='Specify the URL or patter to remove')

    parser_list = subparsers.add_parser('list', help='Lists your current favourites')
    parser_list_group = parser_list.add_mutually_exclusive_group()
    parser_list_group.add_argument('--all', '-a', action='store_true', dest='list_all', help='Lists all groups and their URLs')
    parser_list_group.add_argument('--groups', '-g', action='store_true', help='Lists all groups')
    parser_list_group.add_argument('--urls', '-u', action='store_true', help='Lists all URLs flat')
    parser_list_group.add_argument('--pattern', '-p', help='Lists all groups and URLs matching a given pattern')

    parser_open = subparsers.add_parser('open', help='Opens URLs')
    parser_open.add_argument('--group', '-g', required=False, help='Specify the group to open')
    parser_open.add_argument('--alias', '-a', required=False, help='Specify the URL alias to open')
    parser_open.add_argument('--extend', '-e', required=False, nargs='+', help='Extends the URL')

    parser_rename = subparsers.add_parser('rename', help='Rename groups or aliases')
    parser_rename.add_argument('--old', '-o', dest='old', required=True, help='The old name of the group/alias. No wildcards allowed')
    parser_rename.add_argument('--new', '-n', dest='new', required=True, help='The new name of the group/alias.')
    parser_rename.add_argument('--alias', '-a', action='store_true', required=False, help='Renames the given alias')

    return parser.parse_args()


def main():
    args = parse_args()

    if args.debug:
        LOGGER.setLevel('DEBUG')

    DATABASE = URLFavouriteDatabase()

    if 'browser_path' in DATABASE.data:
        webbrowser.register(config['browser'], None, webbrowser.BackgroundBrowser(config['browser_path']))

    if args.cmd == 'config':
        set_browser(args.browser, args.path)

    elif args.cmd == 'add':
        add_URL(args.group, args.url, args.alias)

    elif args.cmd == 'del':
        pass

    elif args.cmd == 'list':
        pass

    elif args.cmd == 'open':
        pass

    elif args.cmd == 'rename':
        pass
    else:
        LOGGER.error("Wrong usage. See --help/-h for help.")

if __name__ == '__main__':
    main()
