import curses
from tabbed_curses import CursesTabWrapper, TabbedCurses
from terminal_stocks import Command, HistoryDataFetcher


class TimeGraph(Command):

    def __init__(self, config):
        Command.__init__(self, config)
        self._data_fetcher = HistoryDataFetcher()
        self._curzez = TabbedCurses(config['stock_symbols'],
                                    tab_clazz=GraphCurses)

    def execute(self):
        for tab in self._curzez._tabs:
            tab_data = self._data_fetcher.fetch_data(tab._title,
                                                     1,
                                                     1,
                                                     2014,
                                                     'd')
            self.display_data(tab_data, tab)

    def display_data(self, data, tab):
        hor_line_pos, graph_heights = self.data_to_graph(data, tab)
        tab.draw_horizontal_bar_scr_width(hor_line_pos, 5)
        for i, h in enumerate(graph_heights):
            tab.draw_vertical_bar(hor_line_pos,
                                  i + 1,
                                  h,
                                  4 if h < 0 else 3)

    def data_to_graph(self, data, tab):
        max_x = tab._max_x - 2
        max_y = tab._max_y - 2
        all_vals = [float(a['Open']) for a in data] + \
            [float(a['Close']) for a in data]
        min_val = min(all_vals)
        val_range = max(all_vals) - min_val
        gran_x = int(len(data) / (max_x))
        gran_x = 1 if gran_x < 1 else gran_x
        gran_y = (max_y) / val_range
        start_val = float(data[0]['Open'])
        graph_vals = []
        for day in data[1::gran_x]:
            open_val = int((float(day['Open']) - start_val) * gran_y)
            graph_vals.append(open_val)
        return int(max_y - ((start_val - min_val) * gran_y)), graph_vals


class GraphCurses(CursesTabWrapper):

    def init_colors(self):
        CursesTabWrapper.init_colors(self)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_GREEN)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_RED)
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_WHITE)

    def draw_horizontal_bar_scr_width(self, y_pos, color):
        self.draw_horizontal_bar(y_pos,
                                 1,
                                 self._max_x - 3,
                                 color)

    def draw_vertical_bar(self, y_pos, x_pos, height, color):
        if 0 < x_pos < self._max_x and 0 <= y_pos - height <= self._max_y:
            for i in range(y_pos-height, y_pos, 1 if height > 0 else -1):
                self._pad.addstr(i, x_pos, '|', curses.color_pair(color))
            self.refresh()

    def draw_horizontal_bar(self, y_pos, x_pos, length, color):
        if 0 < y_pos < self._max_y and 0 < x_pos + length < self._max_x:
            for i in range(x_pos, x_pos+length, 1 if length > 0 else -1):
                self._pad.addstr(y_pos, i, ' ', curses.color_pair(color))
            self.refresh()


def test():
    try:
        tg = TimeGraph(dict(stock_symbols=['amzn', 'msft', 'aapl', 'goog']))
        tg.execute()
        while tg._curzez.get_ch() != 113:
            pass
    except Exception as e:
        if tg is not None:
            tg._curzez.close_scr()
        print(e)

if __name__ == '__main__':
    test()
