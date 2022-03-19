from abc import ABC


class Event(ABC):
    def __init__(self):
        self._observers = []

    def notify(self, *data):
        for o in self._observers:
            o(*data)

    def attach(self, callback):
        if callback in self._observers:
            return
        self._observers.append(callback)

    def detach(self, callback):
        if callback not in self._observers:
            return
        self._observers.remove(callback)
