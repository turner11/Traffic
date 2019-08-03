from collections import OrderedDict


class Payload(object):
    """"""
    VEHICLE_LABELS = {'motorbike', 'truck', 'bus', 'car'}

    @property
    def vehicle_detections(self):
        return (detection for detection in self.detections if detection.label in self.VEHICLE_LABELS)

    @property
    def original_frame(self):
        return self._original_frame

    def __init__(self, frame=None, detections=None, key_pressed=None, tracking_rois=None, i_frame=None, **args):
        """"""
        super().__init__()
        self._original_frame = frame.copy()
        self.frame = frame
        self.detections = detections or []
        self.tracking_rois = tracking_rois or []
        self.tracking_boxes = []
        self.key_pressed = key_pressed or None
        self.debug_data = OrderedDict()
        self.debug_string = ''
        self.i_frame = i_frame
        self._args = args
        self.dfs = {}
        self.viewables = {}

    def __repr__(self):
        return super().__repr__()

    def __copy__(self):
        cls = self.__class__
        instance = cls.__new__(cls)
        instance.__dict__.update(self.__dict__)
        return instance
