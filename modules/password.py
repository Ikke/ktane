from window import Window
from collections import defaultdict
import string
import curses
import logging

logging.basicConfig(filename='debug.log', level=logging.DEBUG)

class Password(Window):
    def new(self):
        self.columns = [[],[],[],[],[]]
        self.column_pos = [0, 0, 0, 0, 0]
        self.column = 0
        self.title = "Password"

    def _event(self, ev, c):
        nr_letters = 6
        nr_columns = 5
        if c in ['1', '2', '3', '4', '5']:
            self.column = int(c) - 1
        elif c in string.ascii_lowercase:
            cur_column = self.columns[self.column]
            if len(cur_column) < nr_letters:
                cur_column.append(c)
                if len(cur_column) == nr_letters:
                    self.column = (self.column + 1) % nr_columns
        elif ev == curses.KEY_UP:
            column_pos = self.column_pos[self.column]
            column_pos = (column_pos + 1) % nr_letters 
            self.column_pos[self.column] = column_pos
        elif ev == curses.KEY_DOWN:
            column_pos = self.column_pos[self.column]
            column_pos = (column_pos - 1) % nr_letters
            self.column_pos[self.column] = column_pos
        elif ev == curses.KEY_LEFT:
            self.column = (self.column - 1) % nr_columns
        elif ev == curses.KEY_RIGHT or c == " ":
            self.column = (self.column + 1) % nr_columns
        elif ev == curses.KEY_DC:
            self.columns[self.column] = []
        elif ev in [curses.KEY_BACKSPACE, 127]:
            if len(self.columns[self.column]) == 0:
                self.column = (self.column - 1) % nr_columns

            if len(self.columns[self.column]) != 0:
                self.columns[self.column].pop()

    def _update(self, win):
        main_row = 7
        win.erase()
        win.addstr(0, 0, "Password", curses.A_BOLD)
        win.addstr(main_row, 0, "| | | | | |")

        for i, column in enumerate(self.columns):
            active_column = i == self.column
            start_y = main_row - self.column_pos[i]
            x = 1 + i*2

            if len(column) > 0:
                for j, letter in enumerate(column):
                    y = start_y + j
                    attr = 0
                    if active_column and y == main_row:
                        attr = curses.A_BOLD
                    win.addstr(y, x, letter, attr)
            else:
                if active_column:
                    win.addstr(main_row, x, "_", curses.A_BOLD)

        if len(self.columns[0]) > 0:
            cur_char = self.columns[0][self.column_pos[0]]
            if cur_char in positions[0]:
                win.addstr(14, 0, "\n".join(positions[0][cur_char]))

                

words = """
about small
after sound
again spell
below still
could study
every their
first there
found these
great thing
house think
large three
learn water
never where
other which
place world
plant would
point write
right""".strip().split()

positions = [defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)]

for i in range(0, 5):
    for word in words:
        positions[i][word[i]].append(word)
