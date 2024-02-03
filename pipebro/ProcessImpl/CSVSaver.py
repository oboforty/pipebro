import csv
import json

from pipebro import Process, DTYPE
from pipebro.elems.data_types import iterate_dtypes


class CSVSaver(Process):
    """
    CSV & TSV parser
    """
    consumes = object
    produces = str, "filename"

    writer: dict[DTYPE, csv.DictWriter] = {}
    fh: dict = {}

    def initialize(self):
        csv_file = self.cfg.get('files.csv_file')

        self.custom_attr = {}
        self.to_json = {}

        for dtype in iterate_dtypes(self.consumes):
            dtype_cls, dtype_id = dtype

            if hasattr(dtype_cls, 'to_serialize'):
                fieldnames = dtype_cls.to_serialize()
            else:
                fieldnames = set(self.cfg.get(f'csv:{dtype_cls.__name__}.to_serialize'))

            if hasattr(dtype_cls, 'to_json'):
                to_json = dtype_cls.to_json()
            else:
                to_json = self.cfg.get(f'csv:{dtype_cls.__name__}.to_json', default=set(), cast=set)

            if hasattr(dtype_cls, 'custom_attr'):
                custom_attr = dtype_cls.custom_attr()
            else:
                custom_attr = self.cfg.get(f'csv:{dtype_cls.__name__}.custom_attr', default=set(), cast=set)

            quotes = self.cfg.get('dialect.quotes')
            delimiter = self.cfg.get('dialect.delimiter')

            # todo: close file (Dispose?)

            self.fh[dtype] = open(csv_file, 'w', encoding='utf8', newline='')

            self.writer[dtype] = csv.DictWriter(self.fh[dtype], fieldnames=fieldnames, quotechar=quotes, delimiter=delimiter)
            if fieldnames:
                self.writer[dtype].writeheader()

            self.to_json[dtype] = to_json
            self.custom_attr[dtype] = custom_attr

    def dispose(self):
        for dtype, fh in self.fh.items():
            fh.close()

    async def produce(self, data, dtype: DTYPE=None):
        # MN  = self.cfg.get('test.multiply', cast=float, default=1)
        # y = IntWrap(data.val * MN, True)
        # y.__DATAID__ = data.__DATAID__
        #yield y
        if dtype is None:
            dtype = self.consumes

        if dtype not in self.writer:
            raise Exception("Unexpected DTYPE:", dtype)

        to_json = self.to_json[dtype]
        custom_attr = self.custom_attr[dtype]
        view = data.as_dict if hasattr(data, 'as_dict') else dict(data.__dict__)

        # add custom attributes
        for attr in custom_attr:
            view[attr] = getattr(data, attr)

        for field in to_json:
            view[field] = json.dumps(view[field])

        self.writer[dtype].writerow(view)

        yield ".csv"
