from window import Window
import curses
import logging

class Memory(Window):
    def new(self):
        self.stages = []
        self.pos = 0
        self.part = "pos"
        self.title = "Memory"

    def _event(self, ev, c):
        if c == "p":
            self.part = "pos"
        elif c == "l":
            self.part = "lbl"
        elif c in ['1', '2', '3', '4']:
            if len(self.stages) == self.pos:
                self.stages.append(Stage(**{self.part: c}))
            else:
                setattr(self.stages[self.pos], self.part, c)

            self.part = "pos" if self.part == "lbl" else "lbl"
        elif ev in [curses.KEY_ENTER, 10]:
            self.pos = (self.pos +1) % 5
            self.part == "pos"
        elif c == "r":
            self.new()
            
    
    def _update(self, win):
        win.erase()
        win.addstr("Memory\n", curses.A_BOLD)
        win.addstr(table)
        instruction = instructions[self.pos]
        for nr, line in enumerate(instruction.split("\n")):
            win.addstr(2 + nr, 14, line)

        for index, stage in enumerate(self.stages):
            logging.debug("{} {!s}".format(index, stage.pos))
            win.addstr(5 + index * 2, 4, stage.pos)
            win.addstr(5 + index * 2, 8, stage.lbl)

        if self.part == "pos":
            win.addstr(3,4, "P", curses.A_BOLD)
        if self.part == "lbl":
            win.addstr(3,8, "L", curses.A_BOLD)

        win.addstr(5 + self.pos * 2, 0, str(self.pos + 1), curses.A_BOLD)

class Stage():
    def __init__(self, pos="", lbl=""):
        self.pos = pos
        self.lbl = lbl

instructions = [
"""
1 -> 2nd
2 -> 2nd
3 -> 3rd
4 -> 4rth""",
"""
1 -> lbl 4
2 -> pos stg 1
3 -> 1st
4 -> pos stg 1""",
"""
1 -> lbl stg 2
2 -> lbl stg 1
3 -> 3rd
4 -> lbl 4""",
"""
1 -> pos stg 1
2 -> 1st
3 -> pos stg 2
4 -> pos stg 2""",
"""
1 -> lbl stg 1
2 -> lbl stg 2
3 -> lbl stg 4
4 -> lbl stg 3"""
]

table = """
  +---+---+
  | P | L |
  +---+---+
1 |   |   |
  +---+---+
2 |   |   |
  +---+---+
3 |   |   |
  +---+---+
4 |   |   |
  +---+---+"""
