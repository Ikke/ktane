import curses
import logging
from curses import ascii
from modules import *
from utils import Stack, TriState
from window import Window

logging.basicConfig(filename='debug.log', level=logging.DEBUG)


class Bomb(Window):
    def new(self):
        self.parallel = TriState('unknown', 'yes', 'no')
        self.batteries = 'unknown'
        self.serial = TriState('unknown', 'odd', 'even')
        self.vowels = TriState('unknown', 'yes', 'no')
        self.car = TriState('unknown', 'yes', 'no')
        self.frk = TriState('unknown', 'yes', 'no')

        self.notify_list = []

    def notify_on_finish(self, cb):
        self.notify_list.append(cb)

    def __str__(self):
        return "<BombData()>"

    def event(self, ev, c):
        if ascii.isdigit(ev):
            self.batteries = c
        elif c == 'p':
            self.parallel.toggle()
        elif c == 'v':
            self.vowels.toggle()
        elif c == 's':
            self.serial.toggle()
        elif c == 'f':
            self.frk.toggle()
        elif c == 'c':
            self.car.toggle()
        elif ev in [curses.KEY_ENTER, 10]:
            for cb in self.notify_list:
                cb(self)

    def update(self, win):
        win.erase()
        win.move(1,0)
        win.clrtoeol()

        win.addstr("Provide basic bomb information:\n\n")
        win.addstr("Batteries: {}\n".format(self.batteries))
        win.addstr("Parralel:  {}\n".format(self.parallel))
        win.addstr("Serial:    {}\n".format(self.serial))
        win.addstr("Vowels:    {}\n".format(self.vowels))
        win.addstr("FRK:       {}\n".format(self.frk))
        win.addstr("CAR:       {}\n".format(self.car))
        win.addstr("\nPress enter to continue")


class ModuleChooser(Window):
    def update(self, win):
        max_y, max_x = win.getmaxyx()

        x = int(max_x / 2) - 15

        win.erase()
        win.addstr(8, x, "Choose a module:")
        win.addstr(9, x, "1: Simple wires")
        win.addstr(10, x, "2: Button")
        win.addstr(11, x, "3: Memory")
        win.addstr(12, x, "4: Sequence Wires")
        win.addstr(13, x, "5: Password")

    def event(self, ev, c):
        modules = {
            "1": SimpleWires,
            "2": Button,
            "3": Memory,
            "4": SequenceWires,
            "5": Password,
        }

        if c in modules:
            self.parent.set_module(modules[c](self.parent))


class Tabs():
    def __init__(self, y, x, *tabs):
        self.tabs = list(tabs)
        self.active_tab = -1
        self.y = y
        self.x = x

    def add_tab(self, text):
        self.tabs.append(text)

    def remove_tab(self, index):
        if index < len(self.tabs):
            del(self.tabs[index])

    def set_tab(self, index, text):
        if index < len(self.tabs):
            self.tabs[index] = text

    def set_active(self, index):
        self.active_tab = index

    def update(self, win):
        win.move(self.y, self.x)
        win.clrtoeol()

        for i, tab in enumerate(self.tabs):
            if i == self.active_tab:
                if i != 0:
                    win.addstr(" ", curses.A_REVERSE)
                win.addstr("{} ".format(tab), curses.A_REVERSE)
            else:
                if i != 0:
                    win.addstr(" ")
                win.addstr("{} ".format(tab))


class Program:
    def __init__(self):
        self.focus = Stack()
        self.running = False
        self.win = None
        self.s = None
        self.tabs = None
        self.bomb = None

    def init_state(self):
        self.modules = [None, None, None, None, None, None, None, None]
        self.tabs = Tabs(5, 0, *["Empty"] * 8)
        self.focus = Stack()
        self.slot = -1

        bomb = self.bomb = Bomb(self)
        bomb.notify_on_finish(self.bomb_info_finished)
        self.update_bomb_info(bomb)

        chooser = ModuleChooser(self)
        self.focus.push(chooser)

        self.focus.push(bomb)

    def run(self, screen):
        if self.running:
            return
        
        self.running = True
        self.screen = screen

        curses.noecho()
        curses.curs_set(0)

        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        
        max_y, max_y = screen.getmaxyx()

        self.win = win = curses.newwin(50, max_y, 7, 0)
        win.keypad(1)

        self.init_state()

        self.add_decoration()
        self.tabs.update(screen)

        while True:
            logging.debug("Program: Updating current object {:}".format(self.focus.cur()))
            self.focus.cur().update(win)
            logging.debug("Program: Refreshing window")
            screen.refresh()
            win.refresh()

            logging.debug("Program: Waiting for event")
            ev = win.getch()

            if ev == curses.KEY_F12:
                return
            elif ev == curses.KEY_F10:
                if not type(self.focus.cur()) is Bomb:
                    self.slot = -1
                    win.erase()
                    self.focus.push(self.bomb)
            elif ev == curses.KEY_F11:
                self.init_state()
            elif curses.KEY_F1 <= ev <= curses.KEY_F8:
                curses.curs_set(0)
                self.slot = ev - curses.KEY_F1
                logging.debug("Program: Selected module {}".format(self.slot))
                if not type(self.focus.cur()) is ModuleChooser:
                    self.focus.pop()
                if self.modules[self.slot]:
                    logging.debug("Program: Current module active: {!s:}".format(self.focus.cur()))
                    self.focus.push(self.modules[self.slot])
                    self.win.erase()
            else:
                self.focus.cur().event(ev, chr(ev))

            self.tabs.set_active(self.slot) 
            self.tabs.update(screen)

            if self.focus.cur() is None:
                win.addstr(10, 50, "No module active")

    def bomb_info_finished(self, bomb):
        logging.debug("Program: Bomb info finished")
        self.update_bomb_info(bomb)
        if self.slot == -1:
            self.slot = 0

        self.focus.pop()

    def update_bomb_info(self, bomb):
        self.screen.move(1,0)
        self.screen.clrtoeol()
        self.screen.addstr("batteries: {!s: <9} parallel: {}".format(bomb.batteries, bomb.parallel))
        self.screen.move(2,0)
        self.screen.clrtoeol()                       
        self.screen.addstr("serial:    {!s: <9} vowels:   {}".format(bomb.serial, bomb.vowels))
        self.screen.move(3,0)
        self.screen.clrtoeol()
        self.screen.addstr("FRK:       {!s: <9} CAR:      {}".format(bomb.frk, bomb.car))

    def set_module(self, module):
        self.modules[self.slot] = module
        self.tabs.set_tab(self.slot, module.title)
        self.focus.push(module)

    def add_decoration(self):
        self.screen.addstr(0,0, " Keep talking and Nobody Explodes - Manual helper", curses.A_REVERSE | curses.A_BOLD)
        y, x = self.screen.getyx()
        max_y, max_x = self.screen.getmaxyx()
        length = max_x - x
        self.screen.addstr(" " * length, curses.A_REVERSE | curses.A_BOLD)
        self.screen.addstr(6,0, "─" * max_x)

program = Program()
curses.wrapper(program.run)
