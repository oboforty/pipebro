
class AbstractData:
    __DATAID__: object
    __DATALABEL__: str

    def __hash__(self):
        raise NotImplementedError()
        return hash((type(self), self.__DATAID__))

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'<Data #{self.__DATAID__}>'


class NoProd:
    pass
