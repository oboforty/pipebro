from pipebro import Consumer
from pipebro.elems.data_types import repr_dtype


class Debug(Consumer):
    cfg = "EXCLUDE"

    consumes = object

    async def consume(self, data, dtype):
        # if self.app.debug and self.app.verbose:
        print(f"\033[96m DEBUG: {repr_dtype(dtype)} -- {data}\033[00m")


class DebugCount(Consumer):
    cfg = "EXCLUDE"

    consumes = object

    items = []
    def initialize(self):
        self.items = []

    async def consume(self, data, dtype):
        self.items.append(data)

    def dispose(self):
        print(f"\033[96m {self.__PROCESSID__} COUNT: {len(self.items)}\033[00m")
