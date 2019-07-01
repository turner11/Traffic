from copy import copy, deepcopy


class Payload(object):
    """"""

    def __init__(self, frame=None, detections=None, key_pressed=None, tracking_rois=None, **args):
        """"""
        super().__init__()
        self.original_frame = frame
        self.frame = frame
        self.detections = detections or []
        self.tracking_rois = tracking_rois or []
        self.key_pressed = key_pressed or None
        self._args = args

    def __repr__(self):
        return super().__repr__()

    def __copy__(self):
        cls = self.__class__
        instance = cls.__new__(cls)
        instance.__dict__.update(self.__dict__)
        return instance
