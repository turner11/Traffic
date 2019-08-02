class MissingFileException(Exception):
    """"""

    def __init__(self, message):
        """"""
        super().__init__(message)


class ArgumentException(Exception):
    """"""

    def __init__(self, message):
        """"""
        super().__init__(message)

class NoDataException(Exception):
    def __init__(self, *args, **kwargs):
        """"""
        super().__init__(args, kwargs)

    def __repr__(self):
        return super().__repr__()


