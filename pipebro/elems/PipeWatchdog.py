import time

from .PipeEndSignal import PipeEndSignal


class PipeWatchdog:

    def __init__(self, pipe, process_id: str):
        self.pipe = pipe
        self.process_id = process_id
        self.idle_since = time.time()
        self.MAX_IDLE = 0.5
        self.is_idle = False

    def mark_idle(self):
        now = time.time()

        self.is_idle = now - self.idle_since > self.MAX_IDLE
        if self.is_idle:
            print(f"Process {self.process_id} went idle!")
            sgn = PipeEndSignal()
            sgn.processes_idle[self.process_id] = True
            self.pipe.signal(sgn)

    def mark_process_activity(self):

        print("Process Activity", self.process_id)
        self.idle_since = time.time()
