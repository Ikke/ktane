from window import Window
import curses

class SequenceWires(Window):
    def new(self):
        self.positions = {"r": 0, "u": 0, "a": 0}
        self.title = "Sequence"

    def _event(self, ev, c):
        trans = {
            'z': 'r', 'Z': 'R',
            'x': 'u', 'X': 'U', 
            'c': 'a', 'C': 'A'}
        if c in trans:
            c = trans[c]

        if c in ["r", "u", "a"]:
            self.positions[c] += 1
        if c in ["R", "U", "A"]:
            self.positions[c.lower()] -= 1

    def _update(self, win):
        win.erase()
        win.addstr("Sequence Wires\n")
        win.addstr("--------------\n")
        win.addstr(tables)
        win.addstr(4,3, "Red", curses.color_pair(1))
        win.addstr(4,20, "Blue", curses.color_pair(2))

        for index, color in enumerate(['r', 'u', 'a']):
            x = 11 + index * 17
            y = 6 + 2 * self.positions[color]
            win.addstr(y, x, "<--")
        

tables = """
+--------+       +--------+       +--------+
|  Red   |       |  Blue  |       | Black  |
+--------+       +--------+       +--------+
|   C    |       |   B    |       |  Any   |
+--------+       +--------+       +--------+
|   B    |       | A or C |       | A or C |
+--------+       +--------+       +--------+
|   A    |       |   B    |       |   B    |
+--------+       +--------+       +--------+
| A or C |       |   A    |       | A or C |
+--------+       +--------+       +--------+
|   B    |       |   B    |       |   B    |
+--------+       +--------+       +--------+
| A or C |       | B or C |       | B or C |
+--------+       +--------+       +--------+
|  Any   |       |   C    |       | A or B |
+--------+       +--------+       +--------+
| A or B |       | A or C |       |   C    |
+--------+       +--------+       +--------+
|   B    |       |   A    |       |   C    |
+--------+       +--------+       +--------+
"""

