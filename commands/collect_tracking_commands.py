import cv2
from commands.abstract_command import FrameCommand


class TrackDetectionsCommand(FrameCommand):
    """"""

    def __init__(self):
        """"""
        super().__init__(toggle_key='t')
        self._is_on = False

    def _execute(self, payload):
        boxes = (detection.bounding_box for detection in payload.detections)
        boxes = [tuple(box) for box in boxes]
        payload.tracking_rois.extend(boxes)

        # Don't start marking at every frame
        self._is_on = False
        return payload


class ManualTrackingCommand(FrameCommand):
    """"""

    def __init__(self):
        """"""
        super().__init__(toggle_key='m')
        self._is_on = False

    def _execute(self, payload):
        frame = payload.frame
        window_name = 'Set tracking area'
        init_bounding_box = cv2.selectROI(window_name, frame, fromCenter=False, showCrosshair=True)
        cv2.destroyWindow(window_name)

        has_bounding_box = any(v != 0 for v in init_bounding_box)
        if has_bounding_box:
            payload.tracking_rois.append(init_bounding_box)

        # Don't start marking at every frame
        self._is_on = False
        return payload
