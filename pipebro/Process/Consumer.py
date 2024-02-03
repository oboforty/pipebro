from .Process import Process
from pipebro.elems.data_types import DTYPE
from ..elems.PipeEvent import PipeEvent


class Consumer(Process):
    produces = PipeEvent

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def produce(self, *args: tuple[DTYPE]):
        # todo: how to mark and verify if all data has been consumed?
        # for data in args:
        #     print(f'   {self.__PROCESSID__}: Consumed', data)

        yield PipeEvent("end"), (PipeEvent, "end")

    def mark_finished(self):
        self.app.pipe_end_evt.consumers_finished[self.__PROCESSID__] = True
