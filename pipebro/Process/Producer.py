from .Process import Process
from ..elems.data_types import DTYPES
from ..elems.PipeEndSignal import PipeEndSignal
from ..elems.PipeEvent import PipeEvent
from ..elems.AbstractData import AbstractData


class Producer(Process):
    consumes = PipeEvent, "start"

    async def consume(self, data: AbstractData, dtype: DTYPES):
        if self.app.debug:
            assert isinstance(data, PipeEvent) and dtype[1] == 'start'

    def mark_finished(self):
        sgn = PipeEndSignal()

        # a produces immediately goes idle after it marks itself done
        sgn.producers_finished[self.__PROCESSID__] = True
        sgn.processes_idle[self.__PROCESSID__] = True

        self.app.signal(sgn)
