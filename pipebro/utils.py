import functools
import time


def print_progress(st, i, tstart=None, si=None, **kwargs):
    dt = None
    pb = None

    mod4 = (si if si else i) % 4
    if mod4 == 0: pb = '—'
    elif mod4 == 1: pb = '\\'
    elif mod4 == 2: pb = '|'
    elif mod4 == 3: pb = '/'

    if tstart:
        dt = time.time() - tstart
        dt = time.strftime('%H:%M:%S', time.gmtime(dt))

    print("\r", st.format(iter=i, spinner=pb, dt=dt, **kwargs), end="")


class AutoIncrement:
    def __init__(self):
        self.n = 0

    def __call__(self):
        self.n += 1
        return self.n


def get_dict_hierarchy(conf: dict, opts, default=None, cast=None):
    parts = opts.split('.')
    cont = conf

    try:
        for part in parts[:-1]:
            cont = cont[part]
    except Exception as e:
        return default

    last_opt = parts[-1]
    return cont.get(last_opt, default)


class SettingWrapper:
    def __init__(self, conf):
        self.conf = conf

    def __getitem__(self, item):
        return self.conf.get(item)

    def __setitem__(self, item, value):
        self.conf[item] = value

    def __len__(self):
        return len(self.conf)

    def get(self, opts, default=None, cast=None):
        return get_dict_hierarchy(self.conf, opts, default, cast)

    @property
    def view(self):
        return self.conf.copy()

    def __repr__(self):
        return f'<SettingWrapper {repr(self.conf)}>'
