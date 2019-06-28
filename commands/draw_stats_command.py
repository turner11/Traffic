import cv2
from imutils.video import FPS
from commands.abstract_command import FrameCommand


class DrawStatsCommand(FrameCommand):
    """"""



    def __init__(self, additional_info: dict = None):
        """
        :param additional_info: additional info to show
        """
        super().__init__('s')
        self.fps = None
        self.additional_info = additional_info or {}
        self.started = False

    def _execute(self, payload):
        frame = payload.frame
        if not self.started:
            self.fps = FPS().start()
            self.started = True
        else:
            fps = self.fps

            # update the FPS counter
            fps.update()
            fps.stop()

            info = [
                       ("FPS", "{:.2f}".format(fps.fps())),
                   ] + list(self.additional_info.items())

            # output_frame = imutils.resize(frame, width=500)
            (H, W) = frame.shape[:2]
            # loop over the info tuples and draw them on our frame
            for (i, (k, v)) in enumerate(info):
                text = "{}: {}".format(k, v)
                color = (0, 255, 0)
                cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)
        payload.frame = frame
        return payload

    def _is_on_changed(self, is_on):
        super()._is_on_changed(is_on)
        self.fps = None
        self.started = False




