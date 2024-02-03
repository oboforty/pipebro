from .Process import Process
from .AbstractProcess import ProcessWrapper


class Concurrent(Process, ProcessWrapper):
    consumes = None
    produces = None

    def __init__(self, children: list[Process], process_id=None):
        super().__init__(process_id)
        self.children = children

        self.consumes = self.children[0].consumes
        self.produces = self.children[0].produces

        for child in self.children:
            assert child.consumes == self.consumes, "Processes in Concurrent must have matching consumed data"
            assert child.produces == self.produces, "Processes in Concurrent must have matching produced data"

        # todo: later: create a Concurrent that can distribute queues between subsets of `consumes` requirements
