from .AbstractData import AbstractData


class PipeEvent(AbstractData):
    def __init__(self, sg):
        self.__DATAID__ = sg
