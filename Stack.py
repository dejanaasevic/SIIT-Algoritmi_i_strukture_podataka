class StackError(Exception):
    pass


class Stack(object):
    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        if len(self) == 0:
            return True
        return False

    def push(self, element):
        self._data.append(element)

    def top(self):
        if self.is_empty():
            raise StackError("Stack is empty.")
        else:
            return self._data[-1]

    def pop(self):
        if self.is_empty():
            raise StackError("Stack is empty.")
        else:
            elem = self._data[-1]
            del (self._data[-1])
            return elem

