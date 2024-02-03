
class AbstractProcess:

    def __init__(self, process_id=None):
        self.app = None
        self.__PROCESSID__ = process_id if process_id else self.__class__.__name__

    def __repr__(self):
        return repr(self.__PROCESSID__)


class ProcessWrapper(AbstractProcess):
    pass
