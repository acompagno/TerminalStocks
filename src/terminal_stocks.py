from urllib.request import urlopen


class Command:

    def __init__(self, config):
        self._config = config

    def execute(self):
        raise Exception('Error: Execute command not implemented')


class DataFetcher:

    base_url = 'http://download.finance.yahoo.com/d/quotes.csv?s={0}&f={1}'

    def __init__(self, stocks, query):
        self._stocks = stocks
        self._query = query
        self._failed = 0

    def fetch_data(self):
        try:
            url = self.base_url.format(','.join(self._stocks), self._query)
            return urlopen(url).read().decode('utf-8').strip()
        except:
            self._failed += 1
            return None

    def get_failures(self):
        return self._failed
