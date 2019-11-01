import math
import pandas as pd
import numpy as np
from scipy import stats


def add_prev_data(df: pd.DataFrame) -> pd.DataFrame:
    def _add_prev(df_id):
        df_with_previous = df_id[['x', 'y', ]].shift()
        df_ret = df_id.join(df_with_previous, rsuffix='_prev')

        angle = df_ret.apply(lambda row: np.rad2deg(math.atan2(row.y - row.y_prev, row.x - row.x_prev)), axis=1)
        df_ret.loc[:, 'angle'] = (angle + 360) % 360

        df_previous_angle = df_ret[['angle']].shift()
        df_ret = df_ret.join(df_previous_angle, rsuffix='_prev').reset_index(drop=True)

        angle_diff_1 = (df_ret.angle_prev - df_ret.angle + 360) % 360
        angle_diff_2 = (df_ret.angle - df_ret.angle_prev + 360) % 360

        angle_diff = pd.DataFrame(data=[angle_diff_1.values, angle_diff_2.values]).T.min(axis=1)
        df_ret.loc[:, 'angle_diff'] = angle_diff

        return df_ret

    df_with_prev = df.groupby('id').apply(_add_prev).reset_index(drop=True)
    return df_with_prev


def add_distance_data(df: pd.DataFrame) -> pd.DataFrame:
    def _add_distance(df_id):
        df_id.loc[:, 'distance'] = \
            np.sqrt((df_id.x - df_id.x_prev) ** 2 + (df_id.y - df_id.y_prev) ** 2)
        df_id = df_id.dropna()
        df_id.loc[:, 'cum_distance'] = df_id.distance.cumsum()
        return df_id

    df_with_distance = df.groupby('id').apply(_add_distance).dropna().reset_index(drop=True)
    return df_with_distance


def remove_outliers(df: pd.DataFrame, max_z_score: float = 3) -> pd.DataFrame:
    non_outliers = \
        np.bitwise_and.reduce((np.abs(stats.zscore(df[['distance', 'angle_diff']])) < max_z_score), axis=1)
    df_clean = df[non_outliers]
    return df_clean


def smooth(df: pd.DataFrame, window: int = 5, center: bool = False, std: float = 0.2) -> pd.DataFrame:
    def _smooth(df_id):
        df_id.loc[:, 'x'] = df_id.x.rolling(window=window, win_type='gaussian', center=center).mean(std=std)
        df_id.loc[:, 'y'] = df_id.y.rolling(window=window, win_type='gaussian', center=center).mean(std=std)
        df_id = df_id.dropna()
        return df_id

    df_smooth = df.groupby('id').apply(_smooth).reset_index(drop=True)
    return df_smooth


def df_remove_short_series(df):
    groups = df.groupby('id')
    quantiles = groups.agg({'cum_distance': 'max'}).quantile([0.05, 0.1, 0.2, 0.3, 0.4, 0.5])
    df_ret = groups.filter(lambda df_id: max(df_id.cum_distance) > quantiles.loc[0.1].cum_distance)
    return df_ret
