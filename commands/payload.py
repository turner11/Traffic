from collections import OrderedDict
import pandas as pd


class Payload(object):
    """"""

    @property
    def original_frame(self):
        return self._original_frame

    @property
    def fps(self):
        return self.session.get('fps', -1)


    @property
    def elapsed(self):
        return self.i_frame / float(self.fps)

    @property
    def session_data_frames(self):
        return self.session['dfs']

    def __init__(self, frame=None, session=None, detections=None, key_pressed=None, tracking_rois=None, i_frame=None):
        """

        :param frame: The raw frame from video source
        :param session: Information that are are session scoped (not just current frame relevant)
        :param detections:
        :param key_pressed: The key that was pressed in this frame
        :param tracking_rois:
        :param i_frame: The

        """
        super().__init__()
        self.session = session or {}
        self._original_frame = frame.copy()
        self.frame = frame
        self.detections = detections or []
        self.tracking_rois = tracking_rois or []
        self.tracking_boxes = []
        self.key_pressed = key_pressed or None
        self.debug_data = OrderedDict()
        self.debug_string = ''
        self.i_frame = i_frame
        self.dfs = {}
        self.viewables = {}
        self.images = {}

    def get_df_frame_detections(self):
        df = self.session_data_frames.get('detections')
        if df is None:
            df = pd.DataFrame()
        else:
            df = df[df.frame == self.i_frame]
        return df

    def get_session_df(self, key, default_value=None):
        return self.session_data_frames.get(key, default_value)

    def set_session_df(self, key, df):
        self.session_data_frames[key] = df

    def __repr__(self):
        return super().__repr__()

    def __copy__(self):
        cls = self.__class__
        instance = cls.__new__(cls)
        instance.__dict__.update(self.__dict__)
        return instance
