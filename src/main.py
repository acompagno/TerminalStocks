#!/usr/bin/env python2.7

import sys
import json
import argparse
import logging
import stock_ticker
from os.path import expanduser, isfile

config = dict(stock_symbols=[],
              refresh_period=2,
              max_retries=3,
              separator='\n',
              command='stock_ticker',
              no_curses=False)


def main(args):
    logging.basicConfig(filename='/Users/noname/Desktop/example.log',
                        level=logging.DEBUG)
    parse_config_file()
    parse_command_line_args()
    logging.debug(config['no_curses'])
    if config['command'] == 'stock_ticker' and not config['no_curses']:
        command = stock_ticker.StockTickerCurses(config)
    elif config['command'] == 'stock_ticker' and config['no_curses']:
        command = stock_ticker.StockTickerNoCurses(config)
    else:
        print('Invalid command, "{0}" not recognized'.format(config['command']))
        return
    try:
        command.execute()
    finally:
        sys.exit()


def append_config(config_addition):
    for entry in config:
        if entry in config_addition and config_addition[entry] is not None:
            config[entry] = config_addition[entry]


def parse_config_file():
    config_file_location = expanduser("~") + '/.stocks.conf'
    if not isfile(config_file_location):
        return
    config_file = open(expanduser("~") + '/.stocks.conf')
    user_config = json.load(config_file)
    config_file.close()
    append_config(user_config)


def parse_command_line_args():
    args_parser = build_command_line_parser()
    args = vars(args_parser.parse_args())
    logging.debug('Hey {0}'.format(args['no_curses']))
    append_config(args)


def build_command_line_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',
                        '--command',
                        type=str,
                        help='Command that will be executed by the program')
    parser.add_argument('-ss',
                        '--stock_symbols',
                        type=str,
                        nargs='*',
                        help='Stock symbols that the program will display')
    parser.add_argument('-rp',
                        '--refresh_period',
                        type=int,
                        help='Amount of time (in seconds) the program will '
                             + 'wait to fetch new data. Default: 2')
    parser.add_argument('-s',
                        '--separator',
                        type=str,
                        help='String displayed between each stock '
                             + '. Default: \'\\n\'')
    parser.add_argument('-nc',
                        '--no_curses',
                        action='store_true',
                        help='Don\t use curses to display data from '
                             + 'the commands')
    return parser

if __name__ == '__main__':
    main(sys.argv)
