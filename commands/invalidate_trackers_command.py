import pandas as pd
from scipy.spatial import distance
from commands.abstract_command import FrameCommand

# TODO: Change to width/height threshold
THRESHOLD = 10


class InvalidateTrackersCommand(FrameCommand):
    """"""

    def __init__(self, policy_controller=None):
        """"""
        super().__init__(toggle_key='i', policy_controller=policy_controller)

    def _execute(self, payload):
        # Get current frame data
        df_detections = payload.get_session_df('detections')
        df_detections = df_detections[df_detections.frame == payload.i_frame]

        df_tracking = payload.get_session_df('tracking')
        df_tracking = df_tracking[df_tracking.frame == payload.i_frame]

        # merge date
        df_merged = pd.merge(df_detections.assign(key=0), df_tracking.assign(key=0), on='key',
                             suffixes=('_detection', '_tracked')).drop('key', axis=1)
        df_merged = df_merged[df_merged.label_detection == df_merged.label_tracked].reset_index(drop=True)

        df_merged.loc[:, 'center_detection'] = \
            pd.Series((zip(df_merged.x_detection + (df_merged.w_detection / 2.),
                           df_merged.y_detection + (df_merged.h_detection / 2.))))

        df_merged.loc[:, 'center_tracked'] = \
            pd.Series((zip(df_merged.x_tracked + (df_merged.w_tracked / 2.),
                           df_merged.y_tracked + (df_merged.h_tracked / 2.))))

        df_merged.loc[:, 'threshold'] = df_merged[['w_tracked', 'h_tracked']].min(axis=1) / 2

        if len(df_merged):
            df_merged.loc[:, 'distance'] = \
                df_merged.apply(lambda row: distance.euclidean(row.center_detection, row.center_tracked),
                                axis=1)

            df_results = df_merged.groupby('id').agg({'distance': 'min', 'threshold': 'min'}).reset_index()

            # df_invalidate_trackers = df_results[df_results.distance > THRESHOLD]
            idx_within_threshold = df_results.distance <= df_results.threshold
            df_valid_trackers = df_results[idx_within_threshold]

            df_invalidate_trackers = df_tracking[~df_tracking.id.isin(df_valid_trackers.id)]

            df_prev = payload.get_session_df('tracker_invalidation', pd.DataFrame())
            if len(df_prev):
                df_invalidate_trackers = pd.concat([df_prev, df_invalidate_trackers])
            payload.set_session_df('tracker_invalidation', df_invalidate_trackers)
        return payload
