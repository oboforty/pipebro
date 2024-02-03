from queue import SimpleQueue

from pipebro import DTYPE
from .AbstractData import AbstractData


class PipeQueue:
    consumes: DTYPE
    produces: DTYPE

    def __init__(self):
        self.id = None
        self.q: SimpleQueue[tuple[AbstractData, DTYPE]] = SimpleQueue()
    #
    # def put(self, *args, **kwargs):
    #     self.q.put(*args, **kwargs)
    #
    # def get(self, *args, **kwargs):
    #     return self.q.get(*args, **kwargs)

    def __repr__(self):
        return f'<PipeQueue #{self.id}: size={self.q.qsize()}>'
