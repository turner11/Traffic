import cv2
from imutils.video import FPS

OPENCV_OBJECT_TRACKERS = {
        'csrt': cv2.TrackerCSRT_create,
        'mosse': cv2.TrackerMOSSE_create,
        'kcf': cv2.TrackerKCF_create,
        'boosting': cv2.TrackerBoosting_create,
        'mil': cv2.TrackerMIL_create,
        'tld': cv2.TrackerTLD_create,
        'medianflow': cv2.TrackerMedianFlow_create,
    }


class OpenCvTracker(object):
    """"""

    def __init__(self, tracker: str = 'csrt'):
        """"""
        super().__init__()
        self.tracker = tracker
        self.tracker_instance = self._get_tracker(tracker)
        self.started_tracking = False
        self.fps = None

    def _get_tracker(self, tracker):
        ctor = OPENCV_OBJECT_TRACKERS[tracker]
        instance = ctor()
        return instance

    def __repr__(self):
        return f'{self.__class__.__name__}(tracker={self.tracker})'

    def track(self, frame) -> (object, bool):
        tracker = self.tracker_instance

        if not self.started_tracking:
            window_name = 'set tracking area'
            init_bounding_box = cv2.selectROI(window_name, frame, fromCenter=False, showCrosshair=True)
            cv2.destroyWindow(window_name)
            tracker.init(frame, init_bounding_box)
            self.started_tracking = True
            self.fps = FPS().start()

        fps = self.fps

        # grab the new bounding box coordinates of the object
        (success, box) = tracker.update(frame)
        # update the FPS counter
        fps.update()
        fps.stop()

        # check to see if the tracking was a success
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)




        # initialize the set of information we'll be displaying on
        # the frame
        info = [
            ("Tracker", self.tracker),
            ("Success", "Yes" if success else "No"),
            ("FPS", "{:.2f}".format(fps.fps())),
        ]

        # output_frame = imutils.resize(frame, width=500)
        (H, W) = frame.shape[:2]
        # loop over the info tuples and draw them on our frame
        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            color = (0, 255, 0) if success else (0, 0, 255)
            cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        return success, frame

    def reset(self):
        self.tracker_instance = self._get_tracker(self.tracker)
        self.started_tracking = None
        self.fps = None


