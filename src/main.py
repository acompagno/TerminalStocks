#!/usr/bin/env python3

import sys
import json
import stock_ticker
from os.path import expanduser, isfile

config = dict(stock_symbols=[],
              refresh_period=2,
              max_retries=3,
              separator=' | ')


def main(args):
    parse_config_file()
    parse_command_line_args(args)
    command = stock_ticker.StockTicker(config)
    command.execute()
    sys.exit(0)


def parse_config_file():
    config_file_location = expanduser("~") + '/.stocks.conf'
    if not isfile(config_file_location):
        return
    config_file = open(expanduser("~") + '/.stocks.conf')
    user_config = json.load(config_file)
    config_file.close()
    for entry in user_config:
        if entry in user_config:
            config[entry] = user_config[entry]


def parse_command_line_args(args):
    if len(args) < 2:
        return
    config['stock_symbols'] += args[1:]

if __name__ == '__main__':
    main(sys.argv)
