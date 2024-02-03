import os
import sys

if sys.version_info > (3, 10):
    import tomllib

    def load_toml(fn):
        with open(fn, 'rb') as fh:
            return tomllib.load(fh)
else:
    import toml
    load_toml = toml

from .utils import SettingWrapper
from .elems.data_types import DTYPES, DTYPE, repr_dtype
from .Runners.SerialRunner import SerialRunner
from .elems.AbstractData import AbstractData
from .debugging import debug_pipes, draw_pipes_network
from .Process.Process import Process
from .Process.Concurrent import Concurrent
from .Process.Producer import Producer
from .Process.Consumer import Consumer
from .utils import AutoIncrement


class PipeAppBuilder:
    def __init__(self):
        self.cfg_path: str = None
        self.queue_id_fn = AutoIncrement()
        self.processes = []
        self.runner = None

    def add_processes(self, processes, cfg_path=None):
        self.processes.extend(processes)

        if not cfg_path:
            cfg_path = self.cfg_path or ''

        for process in processes:
            if hasattr(process, 'cfg_path'):
                process.cfg_path = cfg_path

            if hasattr(process, 'cfg') and process.cfg != 'EXCLUDE':
                cfg_file_path = os.path.join(cfg_path, process.__PROCESSID__ + '.toml')
                try:
                    process.cfg = SettingWrapper(load_toml(cfg_file_path))
                except Exception as e:
                    raise Exception(f"Error parsing Process config: {cfg_file_path} - {e}")

    def set_runner(self, rid):
        if 'serial' == rid:
            self.runner = SerialRunner
        # elif 'async' == rid:
        #     self.runner = AsyncRunner()

    def build_app(self):
        return self.runner(self.processes)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def pipe_builder(**kwargs):
    return PipeAppBuilder()


__all__ = [
    'pipe_builder',
    'Process', 'Concurrent', 'Producer', 'Consumer',
    'DTYPE', 'DTYPES', 'debug_pipes', 'draw_pipes_network',
    'AbstractData'
]
