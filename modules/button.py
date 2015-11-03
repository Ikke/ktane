from window import Window, LineInput

class Button(Window):
    def new(self):
        self.text = ""
        self.title = "Button"

    def _event(self, ev, char):
        pass

    def _update(self, win):
        win.erase()
        if self.text == "":
            self.input_line("Button: ", ready_callbacks=[self.input_ready])
        else:
            win.addstr("Button: {}\n".format(self.text))
            win.addstr(instructions)


    def input_ready(self, text):
        self.text = text

instructions = """
blue abort                  -> hold
detonate, >1 batteries,     -> release
white, CAR                  -> hold
>2 batteries, FRK           -> release
yellow                      -> hold
red, hold                   -> release
otherwise                   -> hold

blue      -> 4
white     -> 1
yellow    -> 5
otherwise -> 1
"""
