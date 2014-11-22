import time
from ac_curses import color_pairs, CursesWrapper
from threading import Thread, Event
from os import system
from terminal_stocks import DataFetcher, Command


class StockTicker(Command):

    def __init__(self, config):
        Command.__init__(self, config)
        self._data_fetcher = DataFetcher(self._config['stock_symbols'], 'l1p2')

    def execute(self):
        data = self._data_fetcher.fetch_data()
        if data is not None:
            self.display_data(data, self._config['stock_symbols'])
        elif self._data_fetcher.get_failures() == self._config['max_retries']:
            print('Reached max number of failed retries')
            return
        time.sleep(self._config['refresh_period'])

    def parse_data(self, data, stocks):
        parsed_data = []
        split_data = str(data).split('\r\n')
        for stock, price_percentage in zip(stocks, split_data):
            split_price_percentage = price_percentage.split(',')
            price = split_price_percentage[0]
            percentage = split_price_percentage[1].replace('"', '').strip()
            parsed_data.append((stock, price, percentage))
        return parsed_data

    def display_data(self, stock_data, stocks):
        raise Exception('Error: \'display_data\' method not implemented')


class StockTickerCurses(StockTicker, Thread):

    def __init__(self, config):
        StockTicker.__init__(self, config)
        Thread.__init__(self)
        self._curzez = CursesWrapper()
        self._stopper = Event()

    def run(self):
        while not self._stopper.is_set():
            StockTicker.execute(self)

    def execute(self):
        self.start()
        while not self._stopper.is_set():
            input_ch = self._curzez.get_ch()
            if input_ch is None or input_ch == 113:
                break
        self._stopper.set()
        try:
            self.join()
        finally:
            self._curzez.close_scr()

    def display_data(self, stock_data, stocks):
        self._curzez.clear_pad()
        parsed_data = self.parse_data(stock_data, stocks)
        for stock in parsed_data:
            color = color_pairs.GREEN if '+' in stock[2] else \
                color_pairs.RED if '-' in stock[2] else color_pairs.DEFAULT
            self._curzez.write('{0} '.format(stock[0].upper()))
            self._curzez.write('{0} ({1})'.format(stock[1],
                                                  stock[2]),
                               color=color)
            self._curzez.write(self._config['separator'])


class StockTickerNoCurses(StockTicker):

    def __init__(self, config):
        StockTicker.__init__(self, config)

    def execute(self):
        try:
            while True:
                StockTicker.execute(self)
        finally:
            system('clear')

    def display_data(self, stock_data, stocks):
        parsed_data = self.parse_data(stock_data, stocks)
        texts = []
        for stock in parsed_data:
            color = term_colors.GREEN if '+' in stock[2] else \
                term_colors.RED if '-' in stock[2] else term_colors.DEFAULT
            texts.append('{0} {1}{2} ({3}){4}'.format(stock[0].upper(),
                                                      color,
                                                      stock[1],
                                                      stock[2],
                                                      term_colors.DEFAULT))
        system('clear && printf "\e[3J"')
        print(self._config['separator'].join(texts))


class term_colors:

    GREEN = '\033[92m'
    RED = '\033[91m'
    DEFAULT = '\033[0m'

if __name__ == '__main__':
    pass
