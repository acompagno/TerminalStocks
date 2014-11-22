import curses


class color_pairs:

    DEFAULT = 0
    GREEN = 1
    RED = 2


class CursesWrapper:

    def __init__(self):
        self.init_scr()
        self.init_pad()
        self.init_colors()

    def init_scr(self):
        self._scr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self._scr.keypad(1)

    def init_pad(self):
        self._max_y, self._max_x = self._scr.getmaxyx()
        self._pad = curses.newpad(self._max_y * 2, self._max_x * 2)
        self._pad_row_pos = 0
        self._pad_col_pos = 0
        self._scr.refresh()
        self.refresh_pad(self._pad_row_pos,
                         self._pad_col_pos)
        self._pad.keypad(1)

    def init_colors(self):
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)
        curses.init_pair(2, curses.COLOR_RED, -1)

    def close_scr(self):
        curses.nocbreak()
        self._scr.keypad(0)
        curses.echo()
        curses.endwin()

    def refresh(self):
        self.refresh_pad(self._pad_row_pos,
                         self._pad_col_pos)

    def refresh_pad(self, row_pos, col_pos):
        self._pad.refresh(row_pos,
                          col_pos,
                          0,
                          0,
                          self._max_y - 1,
                          self._max_x - 1)

    def get_ch(self):
        try:
            input_ch = self._scr.getch()
        except:
            return None
        if input_ch == curses.KEY_UP:
            self.scroll_up()
        elif input_ch == curses.KEY_DOWN:
            self.scroll_down()
        elif input_ch == curses.KEY_RIGHT:
            self.scroll_right
        elif input_ch == curses.KEY_LEFT:
            self.scroll_left
        elif input_ch == -1 or input_ch == 410:
            self.on_resize()
        return input_ch

    def on_resize(self):
        self._max_y, self._max_x = self._scr.getmaxyx()
        self.refresh()

    def clear_pad(self):
        self._pad.erase()

    def write(self, string, color=color_pairs.DEFAULT):
        self._pad.addstr(string, curses.color_pair(color))
        self.refresh()

    def scroll_up(self):
        if self._pad_row_pos > 0:
            self.scroll(-1, 0)

    def scroll_down(self):
        cur_y = self._pad.getyx()[0]
        if cur_y > self._max_y and cur_y > self._pad_row_pos + self._max_y:
            self.scroll(1, 0)

    def scroll_left(self):
        self.scroll(0, -1)

    def scroll_right(self):
        self.scroll(0, 1)

    def scroll(self, increment_row, increment_col):
        self._pad_row_pos += increment_row
        self._pad_col_pos += increment_col
        self.refresh()


def test():
    r = [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]
    ac_curses = CursesWrapper()
    c = 0
    while True:
        a = ac_curses.get_ch()
        if a not in r:
            ac_curses._pad.addstr(c, 0, 'hellloww' + str(c))
            ac_curses.refresh()
            c += 1

if __name__ == '__main__':
    test()
