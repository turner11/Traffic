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

    def get_scaled(self, factor: float) -> object:
        w = round(self.w * factor)
        h = round(self.h * factor)
        x = self.x + w  # +(w * factor)
        y = self.y + h  # +(h * factor)

        return BoundingBox(x, y, w, h)

    def __repr__(self):
        return f'{self.__class__.__name__}(self.x={self.x}, self.y={self.y}, self.w={self.w}, self.h={self.h})'

    def __iter__(self):
        for val in (self.x, self.y, self.w, self.h):
            yield val


class LabeledBoundingBox(BoundingBox):
    """"""

    def __init__(self, label, x, y, w, h):
        """"""
        super().__init__(x, y, w, h)
        self.label = label

    def __repr__(self):
        return f'{self.__class__.__name__}(self.label={self.label}, ' \
            f'self.x={self.x}, ' \
            f'self.y={self.y}, ' \
            f'self.w={self.w}, ' \
            f'self.h={self.h})'


class Detection(object):
    """"""

    def __init__(self, label, bounding_box, confidence):
        """"""
        super().__init__()
        self.label = label
        self.bounding_box = bounding_box
        self.confidence = confidence

    def __repr__(self):
        return f'{self.__class__.__name__}(label={self.label}, bounding_box={self.bounding_box}, confidence={self.confidence})'

    def __iter__(self):
        return iter(self.bounding_box)


class TrackedBoundingBox(LabeledBoundingBox):
    """"""

    def __init__(self, identifier, label, x, y, w, h):
        """"""
        super().__init__(label, x, y, w, h)
        self.identifier = identifier

    def __repr__(self):
        return f'{self.__class__.__name__}(identifier={self.identifier}, ' \
            f'self.label={self.label}, ' \
            f'self.x={self.x}, ' \
            f'self.y={self.y}, ' \
            f'self.w={self.w}, ' \
            f'self.h={self.h})'


