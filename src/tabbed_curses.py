import curses
from ac_curses import CursesWrapper


class CursesTabWrapper(CursesWrapper):

    def __init__(self, title, super_scr, scroll_enabled=True, pad_multiplier=2):
        self._title = title
        self._scr = super_scr
        CursesWrapper.init_pad(self, pad_multiplier)

    def init_pad(self, pad_multiplier):
        self._max_y, self._max_x = self._scr.getmaxyx()
        self._pad = curses.newpad((self._max_y - 1) * pad_multiplier,
                                  (self._max_x - 1) * pad_multiplier)
        self._pad_row_pos = 0
        self._pad_col_pos = 0
        self._scr.refresh()
        self.refresh_pad(self._pad_row_pos,
                         self._pad_col_pos)
        self._pad.keypad(1)

    def refresh_pad(self, row_pos, col_pos):
        self._pad.refresh(row_pos,
                          col_pos,
                          1,
                          1,
                          self._max_y - 1,
                          self._max_x - 1)


class TabbedCurses:

    def __init__(self, tab_titles, tab_clazz=CursesTabWrapper):
        self._tab_titles = tab_titles
        self._curr_tab = 0
        CursesWrapper.init_scr(self)
        self._tabs = [tab_clazz(title, self._scr)
                      for title in tab_titles]
        tab_clazz.init_colors(self)
        self._tabs[0].refresh()
        self.draw_header()

    def close_scr(self):
        curses.nocbreak()
        self._scr.keypad(0)
        curses.echo()
        curses.endwin()

    def draw_header(self):
        self._scr.move(0, 0)
        self._scr.clrtoeol()
        beg, end = self.split_header(self._curr_tab)
        curr_title = self._tab_titles[self._curr_tab]
        self._scr.addstr(' | '.join(beg))
        if len(beg) > 0:
            self._scr.addstr(' | ')
        self._scr.addstr(curr_title, curses.color_pair(2))
        if len(end) > 0:
            self._scr.addstr(' | ')
        self._scr.addstr(' | '.join(end))

    def split_header(self, index):
        return self._tab_titles[0:index], self._tab_titles[index+1:]

    def next_tab(self):
        if self._curr_tab + 1 < len(self._tabs):
            self._curr_tab += 1
        elif self._curr_tab + 1 == len(self._tabs):
            self._curr_tab = 0
        self._tabs[self._curr_tab].refresh()
        self.draw_header()

    def last_tab(self):
        if self._curr_tab == 0:
            self._curr_tab = len(self._tab_titles) - 1
        else:
            self._curr_tab -= 1
        self._tabs[self._curr_tab].refresh()
        self.draw_header()

    def get_ch(self):
        tab_res = self._tabs[self._curr_tab].get_ch()
        if tab_res == 78 or tab_res == 110:
            self.next_tab()
        elif tab_res == 98 or tab_res == 66:
            self.last_tab()


def test():
    a = TabbedCurses(['hey', 'how', 'are', 'you'])
    while True:
        a.get_ch()
        a.next_tab()
    CursesWrapper.close_scr(a)

if __name__ == '__main__':
    test()
