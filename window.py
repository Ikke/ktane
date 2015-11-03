import logging
import curses
from curses import ascii


KEY_BACKSPACE = 127
KEY_ENTER = 10

class Window():
    def __init__(self, parent):
        self.parent = parent
        self.input = None
        self.title = "Unknown"
        self.new()

    def __str__(self):
        return "{}(Display)".format(self.__class__.__name__)

    def new(self):
        pass

    def event(self, event, char):
        if self.input:
            self.input.event(event, char)
        else:
            self._event(event, char)

    def _event(self, event, char):
        pass

    def update(self, win):
        if self.input:
            self.input.update(win)
        else:
            self._update(win)
            if self.input:
                self.input.update(win)

    def _update(self, win):
        pass

    def input_line(self, *args, ready_callbacks=[], **kwargs):
        logging.debug("Display: Setting up line input")
        ready_callbacks.append(self.input_finished)
        line_input = LineInput()
        line_input.input(*args, ready_callbacks=ready_callbacks, **kwargs)
        self.input = line_input

    def input_finished(self, text):
        self.input = None

class LineInput():
    def __init__(self):
        self.prompt = ""
        self.text = ""
        self.start_coords = None

    def __str__(self):
        return "<LineInput(win)>"
    
    def input(self, prompt, coords=None, ready_callbacks=[], text=""):
        self.ready_callbacks = ready_callbacks
        self.prompt = prompt
        self.text = text
        self.start_coords = coords

    def event(self, ev, c):
        if ascii.isprint(ev):
            self.text += c
        elif ev in [curses.KEY_BACKSPACE, KEY_BACKSPACE]:
            self.text = self.text[:-1]
        elif ev in [curses.KEY_ENTER, KEY_ENTER]:
            curses.curs_set(0)
            logging.debug("LineInput: Enter pressed, {} callbacks".format(len(self.ready_callbacks)))
            for cb in self.ready_callbacks:
                cb(self.text)
        else:
            self.text += c

    def update(self, win):
        win.erase()
        if self.start_coords is None:
            self.start_coords = win.getyx()

        win.move(*self.start_coords)
        win.clrtoeol()
        win.addstr(self.prompt)
        win.addstr(self.text)
        curses.curs_set(1)
