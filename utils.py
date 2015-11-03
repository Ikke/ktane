
class TriState():
    def __init__(self, *options):
        options = list(options)
        self.indeterminate = options.pop(0)
        self.options = options
        self.index = 0
        self.value = self.indeterminate

    def toggle(self):
        self.index = (self.index + 1) % len(self.options)
        self.value = self.options[self.index]
        return self.current

    def indeterminate(self):
        self.current = self.indeterminate
        return self.current

    def current(self):
        return self.value

    def __str__(self):
        return str(self.current())


class Stack():
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.insert(0, item)

    def pop(self):
        return self.stack.pop(0)

    def cur(self):
        return self.stack[0] if len(self.stack) else None

