from collections import namedtuple

Point = namedtuple('Point', ('x', 'y'))


class BoundingBox(object):
    """"""

    @property
    def upper_left(self):
        return Point(self.x, self.y)

    @property
    def lower_right(self):
        return Point(self.x + self.w, self.y + self.h)

    def __init__(self, x, y, w, h):
        """"""
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __repr__(self):
        return f'{self.__class__.__name__}(self.x={self.x}, self.y={self.y}, self.w={self.w}, self.h={self.h})'

    def __iter__(self):
        for val in (self.x, self.y, self.w, self.h):
            yield val


class TrackedBoundingBox(BoundingBox):
    """"""

    def __init__(self, identifier, x, y, w, h):
        """"""
        super().__init__(x, y, w, h)
        self.identifier = identifier

    def __repr__(self):
        return f'{self.__class__.__name__}(identifier={self.identifier}, ' \
                                           f'self.x={self.x}, ' \
                                           f'self.y={self.y}, ' \
                                           f'self.w={self.w}, ' \
                                           f'self.h={self.h})'
