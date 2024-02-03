from abc import abstractmethod
from collections import defaultdict
from typing import AsyncGenerator

from .AbstractProcess import AbstractProcess
from ..elems.data_types import DTYPES, DTYPE, DTYPE_LABEL_REMAP, ismultiple, validate_data, remap_dtype, \
    repr_dtype
from ..elems.AbstractData import AbstractData
from ..elems.PipeQueue import PipeQueue


class Process(AbstractProcess):
    """
    multiple data-type OR data-type OR data-type without label
    """
    cfg = None
    cfg_path: str = None

    consumes: DTYPES
    produces: DTYPES

    def __init__(self, process_id = None, consumes: DTYPE_LABEL_REMAP = None, produces: DTYPE_LABEL_REMAP = None):
        super().__init__(process_id)

        self.cons_ismultiple = ismultiple(self.consumes)
        self.prod_ismultiple = ismultiple(self.produces)
        self.datagroups: dict[object, list] = defaultdict(list)
        self.queue: PipeQueue

        if consumes:
            self.consumes = remap_dtype(self.consumes, consumes)

        if produces:
            self.produces = remap_dtype(self.produces, produces)

    def initialize(self):
        pass

    def dispose(self):
        pass

    #@abstractmethod
    async def consume(self, data: AbstractData, dtype: DTYPES):
        pass

    @abstractmethod
    async def produce(self, *args) -> tuple[AbstractData, DTYPES]:
        pass

    def debug_data(self, evt, data: AbstractData, dtype: DTYPE):
        # TODO: move to debug function/module
        if isinstance(data, dict):
            # silent debug dicts
            _repr = 'dict='+', '.join(map(str, list(data.keys())[:8])) + '...'
        else:
            _repr = repr(data)
        #  :=\n   {_repr}
        print(f"   [{self.__PROCESSID__}] {evt}: {repr_dtype(dtype)}")

        print(dtype)
        assert validate_data(data, dtype)
        assert not ismultiple(dtype), f"{self.__PROCESSID__} {evt}'d multiple DTYPE! Please consume and produce scalar types"

    def __repr__(self):
        return f'<{self.__class__.__name__} #{self.__PROCESSID__}>'

    def __hash__(self):
        return hash(self.__PROCESSID__)
