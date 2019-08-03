import cv2
from commands.abstract_command import FrameCommand
from commands.policy_controller import AutoTurnOffPolicy
from common.types import LabeledBoundingBox


class TrackDetectionsCommand(FrameCommand):
    """"""
    LABELS_TO_TRACK = {'motorbike', 'bicycle', 'stop sign', 'truck', 'bus', 'car', 'person', 'cat', 'dog', 'horse',
                       'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag',
                       'suitcase', 'cell phone', }  # 'traffic light'
    def __init__(self):
        """"""
        super().__init__(toggle_key='t')

    def _execute(self, payload):
        relevant_detections = (detection for detection in payload.detections if detection.label in self.LABELS_TO_TRACK)
        # boxes =(LabeledBoundingBox(detection.label, *detection.bounding_box) for detection in relevant_detections)
        boxes = relevant_detections
        # half size
        # factor = 1/2
        # boxes = ((detection.label, detection.bounding_box.get_scaled(factor)) for detection in boxes)
        # boxes = (LabeledBoundingBox(lbl, *bb) for lbl, bb in boxes)
        payload.tracking_rois.extend(boxes)

        # Don't start marking at every frame
        self.is_on = False
        return payload


class ManualTrackingCommand(FrameCommand):
    """"""

    def __init__(self, policy_controller=None):
        """"""
        policy_controller = policy_controller or AutoTurnOffPolicy()
        super().__init__(toggle_key='m', policy_controller=policy_controller)
        self.is_on = False

    def _execute(self, payload):
        frame = payload.frame
        window_name = 'Set tracking area'
        init_bounding_box = cv2.selectROI(window_name, frame, fromCenter=False, showCrosshair=True)
        cv2.destroyWindow(window_name)

        has_bounding_box = any(v != 0 for v in init_bounding_box)
        if has_bounding_box:
            bounding_box = LabeledBoundingBox('manual', *init_bounding_box)
            payload.tracking_rois.append(bounding_box)

        # Don't start marking at every frame
        self.is_on = False
        return payload
