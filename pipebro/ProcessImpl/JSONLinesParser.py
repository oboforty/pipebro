from pipebro import Process
import json


class JSONLinesParser(Process):
    """
    json lines parser
    """
    consumes = str, "filename"
    produces = dict

    def initialize(self):
        self.filename = self.cfg.get('settings.filename')

    async def produce(self, data: dict):
        with open(self.filename) as fh:
            for line in fh:
                yield json.loads(line), self.produces

    def dispose(self):
        pass
