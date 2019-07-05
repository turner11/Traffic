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
        return f'{self.__class__.__name__}(self.x={self.x}, self.x={self.y}, self.x={self.w}, self.x={self.h})'

    def __iter__(self):
        for val in (self.x, self.y, self.w, self.h):
            yield val
