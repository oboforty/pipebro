import time
from collections import defaultdict
from typing import AsyncGenerator

from ..Process.Process import Process
from ..elems import AbstractData
from ..elems.AbstractData import NoProd
from ..elems.PipeEvent import PipeEvent
from ..elems.data_types import DTYPE, iterate_dtypes, ismultiple, repr_dtype
from ..utils import print_progress


class SerialRunner:

    def __init__(self, processes: list[Process]):
        """
        SerialRunner immediately executes the consumer for all produced data
        This means complete lack of queues and SerialRunner is ideal for simple pipelines
        with few branching processes
        """
        self.cons_flow: dict[DTYPE, set[Process]] = defaultdict(set)
        self.start_event: tuple[PipeEvent, DTYPE] = PipeEvent("start"), (PipeEvent, "start")
        self.debug = False
        self.verbose = False
        self.t1 = None

        self.processes = processes

        proc: Process
        for proc in processes:
            if hasattr(proc, 'app'):
                proc.app = self

            for dtype in iterate_dtypes(proc.consumes):
                self.cons_flow[dtype].add(proc)

    def start_flow(self, start_event, dtype: DTYPE, debug=None, verbose=None):
        self.start_event = start_event, dtype

        if debug is not None: self.debug = debug
        if verbose is not None: self.verbose = verbose

    async def run(self):
        self.t1 = time.time()

        for proc in self.processes:
            proc.initialize()

        await self.consume_data_recursive(*self.start_event)

        for proc in self.processes:
            proc.dispose()

        print("\n\nFinished!", time.time() - self.t1)

    async def consume_data_recursive(self, in_data: AbstractData, in_dtype: DTYPE):
        for proc in self.cons_flow[in_dtype]:
            if self.verbose:
                proc.debug_data('CONS', in_data, in_dtype)
            await proc.consume(in_data, in_dtype)

            if proc.cons_ismultiple:
                resp = proc.produce(in_data, in_dtype)
            else:
                resp = proc.produce(in_data)

            # check if it produced more data
            if isinstance(resp, AsyncGenerator):
                async for prod in resp:
                    if isinstance(prod, tuple) and isinstance(prod[1], tuple) and isinstance(prod[1][0], (tuple, type)):
                        out_data, out_dtype = prod
                    elif proc.prod_ismultiple:
                        if isinstance(prod, tuple):
                            out_data, out_dtype = prod
                        else:
                            try:
                                out_data = prod
                                out_dtype = next(filter(lambda p: p[0] is type(prod), proc.produces))
                            except StopIteration:
                                out_data, out_dtype = prod, type(prod)
                    else:
                        out_data, out_dtype = prod, proc.produces

                    if isinstance(out_data, NoProd):
                        # Producer marks that it didn't produce anything
                        continue

                    if self.verbose:
                        proc.debug_data('PROD', out_data, out_dtype)
                    await self.consume_data_recursive(out_data, out_dtype)

    def print_progress(self, i):
        if not self.verbose:
            if not hasattr(self, 'print_called'):
                self.print_called = 0

            self.print_called += 1
            print_progress("{spinner} {dt}    Processing... {iter}", i=i, si=self.print_called, tstart=self.t1)

    def print_flow(self):
        # TODO: move to debug function/module
        for dtype, processes in self.cons_flow.items():
            print(repr_dtype(dtype))

            for process in processes:
                print(f"   --> [{process.__PROCESSID__}]")

    def signal(self, *args, **kwargs):
        pass
