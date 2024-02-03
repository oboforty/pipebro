

class PipeEndSignal:
    def __init__(self):
        self.producers_finished = {}
        self.consumers_finished = {} # todo: @later
        self.processes_idle = {}

        #self.AllProcessesIdle = False
        #self.EmptyQueues = True # todo: @later

    def __add__(self, other):
        this = PipeEndSignal()

        for k,v in self.producers_finished.items():
            this.producers_finished[k] = v or other.producers_finished.get(k, False)
        for k,v in self.consumers_finished.items():
            this.consumers_finished[k] = v or other.consumers_finished.get(k, False)
        for k,v in self.processes_idle.items():
            this.processes_idle[k] = v or other.processes_idle.get(k, False)

        #this.AllProcessesIdle = self.AllProcessesIdle or other.AllProcessesIdle
        #this.EmptyQueues = self.EmptyQueues or other.EmptyQueues

        return this

    def all_finished(self):
        return all(self.processes_idle.values()) and self.leaves_finished()

    def leaves_finished(self):
        return all(self.producers_finished.values()) and\
               all(self.consumers_finished.values())

    def process_done(self, pid):
        return self.processes_idle[pid] and self.leaves_finished()

    def __repr__(self):
        f = []

        # if self.EmptyQueues:
        #     f.append('Queues Empty')
        # if self.AllProcessesIdle:
        #     f.append('Processes Idle')

        pfin = list(filter(lambda k: self.producers_finished[k], self.producers_finished))
        cfin = list(filter(lambda k: self.consumers_finished[k], self.consumers_finished))
        ffin = list(filter(lambda k: self.processes_idle[k], self.processes_idle))

        if pfin:
            e = ' '.join(pfin)
            f.append(f'Prod {e} Fin')

        if cfin:
            e = ' '.join(cfin)
            f.append(f'Cons {e} Fin')

        if ffin:
            e = ' '.join(ffin)
            f.append(f'Process {e} Idle')

        return '; '.join(f)
