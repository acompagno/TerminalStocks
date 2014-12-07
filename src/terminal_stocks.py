from urllib.request import urlopen
from datetime import date


class Command:

    def __init__(self, config):
        self._config = config

    def execute(self):
        raise Exception('Error: Execute command not implemented')


class DataFetcherBase:

    def __init__(self):
        self._failed = 0

    def curl(self, url):
        try:
            return urlopen(url).read().decode('utf-8').strip()
        except:
            self._failed += 1
            return None

    def get_failures(self):
        return self._failed


class DataFetcher(DataFetcherBase):

    base_url = 'http://download.finance.yahoo.com/d/quotes.csv?s={0}&f={1}'

    def __init__(self, stocks, query):
        DataFetcherBase.__init__(self)
        self._stocks = stocks
        self._query = query

    def fetch_data(self):
        url = self.base_url.format(','.join(self._stocks), self._query)
        return self.curl(url)


class HistoryDataFetcher(DataFetcherBase):

    """
    {0} -> Labels  Ex. GOOG, AAPL, AMZ, etc
    Start Date
        {1} -> Month   Ex. Jan(0) to Dec(11)
        {2} -> Day
        {3} -> Year
    End Date
        {4} -> Month   Ex. Jan(0) to Dec(11)
        {5} -> Day
        {6} -> Year
    {7} -> Interval  Ex. Daily(d), Weekly(w), Monthly(m)

    """
    base_url = 'http://ichart.yahoo.com/table.csv?s={0}&a={1}&b={2}&c={3}' \
               + '&d={4}&e={5}&f={6}&g={7}&ignore=.csv'

    def fetch_data(self, stock, start_month, start_day, start_year, period):
        end_month, end_day, end_year = self.get_current_date_info()
        url = self.base_url.format(stock,
                                   start_month,
                                   start_day,
                                   start_year,
                                   end_month,
                                   end_day,
                                   end_year,
                                   period)
        return self.parse_data(self.curl(url))

    def parse_data(self, data):
        parsed_data = []
        split_data = data.split('\n')
        titles = split_data[0].split(',')
        for line in reversed(split_data[1:]):
            parsed_data.append(dict(zip(titles, line.split(','))))
        return parsed_data

    def get_current_date_info(self):
        today = date.today()
        return today.month - 1, today.day, today.year


def test():
    df = HistoryDataFetcher()
    a = df.fetch_data('goog', 0, 1, 2013, 'm')
    print(a)


if __name__ == '__main__':
    test()
