from window import Window, LineInput

class SimpleWires(Window):
    def new(self):
        self.wires = ""
        self.nr_of_wires = 0
        self.text = ""
        self.title = "Wires"

    def input_ready(self, line):
        self.wires = line
        self.nr_of_wires = len(line.split())
        self.text = "Counted {} wires\n".format(self.nr_of_wires)

    def _event(self, ev, c):
        if c == "n":
            self.wires = ""
            self.nr_of_wires = ""
        if c in ['e', 'n']:
            self.input_line("Wires: ", 
                ready_callbacks=[self.input_ready],
                coords=(0,0),
                text=self.wires
            )

    def translate_wires(self, wires):
        translation = {'u': "blue", 'a': "black", 'r': "red", 'y': "yellow", 'w': "white"}
        return " ".join(translation.get(wire, wire) for wire in wires.split())

    def _update(self, win):
        win.erase()
        if self.wires == "":
            self.input_line("Wires: ", ready_callbacks=[self.input_ready])
        else:
            win.addstr("Wires: {}\n\n".format(self.translate_wires(self.wires)))
            win.addstr(self.text)
            if 2 < self.nr_of_wires < 7:
                win.addstr(instructions[self.nr_of_wires])
            else:
                win.addstr("Number of wires out of range")


instructions = {
    3: """
3 wires
"~~~~~~ 
No red     -> 2 
Last white -> last 
>1 blue    -> last blue 
otherwise  -> last""",
    4: """
4 wires
~~~~~~~
>1 red, serial odd      -> last red
last yellow, no red     -> first wire
=1 blue                 -> first wire
>1 yellow               -> last wire
otherwise               -> second wire
""",
    5: """
5 wires
~~~~~~~
last black, odd         -> fourth wire
=1 red, >1 yellow       -> first wire
=0 black                -> second wire
otherwise               -> first wire
""",
    6: """
6 wires
~~~~~~~
=0 yellow, odd          -> third wire
=1 yellow, >1 white     -> fourth wire
=0 red                  -> last wire
otherwise               -> fourth wire
""",
}

