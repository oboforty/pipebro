from pipebro import Process
import json


class JSONLinesSaver(Process):
    """
    json lines saver
    """
    consumes = dict
    produces = int, "saved"

    def initialize(self):
        self.filename = self.cfg.get('settings.filename')
        self.fh = open(self.filename, 'w')
        self.saved = 0

    async def produce(self, data: dict):
        json.dump(data, self.fh)
        self.fh.write('\n')

        self.saved += 1
        yield self.saved, self.produces

    def dispose(self):
        if self.app.verbose:
            print("JSON Lines Saver: disposing")
        self.fh.close()
