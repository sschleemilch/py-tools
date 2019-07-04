from platform import uname
from os import environ, path
import sys
sys.path.append(path.join(path.dirname(path.abspath(__file__)), '..', 'lib'))
from lib.print.pretty import *
from lib.print.color_string import Color

import argparse

args = None


def parse_args():
    global args
    parser = argparse.ArgumentParser(prog='SYSTEM')
    parser.add_argument('-e', '--environment-vars', action='store_true',
                        dest='environment_vars', help='Lists all set environment variables')
    parser.add_argument('-p', '--python-infos', action='store_true',
                        dest='python', help='Lists information about the python installation')
    args = parser.parse_args()


def print_system_infos():
    printer = Printer(box_color=Color.blue)
    system_information = uname()
    printer.title('System information', color=Color.blue)
    printer.print('SYSTEM', color=Color.blue)
    printer.print(system_information[0], offset=4, color=Color.grey)
    printer.print('OS-VERSION', color=Color.blue)
    printer.print(system_information[3], offset=4, color=Color.grey)
    printer.print('ARCH', color=Color.blue)
    printer.print(system_information[4], offset=4, color=Color.grey)
    printer.print('MACHINE-NAME', color=Color.blue)
    printer.print(system_information[1], offset=4, color=Color.grey)
    printer.print('PROCESSOR', color=Color.blue)
    printer.print(system_information[5], offset=4, color=Color.grey)
    printer.divider()


def print_python_infos():
    printer = Printer(box_color=Color.magenta)
    printer.title('Python installation', color=Color.magenta)
    printer.print('PYTHON-VERSION', color=Color.magenta)
    printer.print(sys.version, offset=4, color=Color.grey)
    printer.print('PYTHON-PATHS', color=Color.magenta)
    for p in sys.path:
        printer.print(p, offset=4, color=Color.grey)
    printer.divider()


def print_environment_vars():
    printer = Printer(box_color=Color.cyan, content_color=Color.cyan)
    printer.title('Environment Variables')
    all_environment_vars = environ

    for ev_name, content in all_environment_vars.items():
        printer.print(ev_name)
        content_entries = content.split(';')
        for ce in content_entries:
            printer.print(ce, color=Color.grey, offset=4)

    printer.divider()


def main():
    parse_args()
    print_system_infos()
    if args.python:
        print_python_infos()
    if args.environment_vars:
        print_environment_vars()


if __name__ == '__main__':
    main()
