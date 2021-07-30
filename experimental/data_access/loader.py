import pandas as pd
import pyarrow.parquet as pq
from functools import lru_cache
import logging
from .source import data_augmentation as aug

logger = logging.getLogger(__name__)

@lru_cache(1)
def load_data(path: str) -> pd.DataFrame:
    logger.debug(f'Loading data from {path}')
    data_set = pq.ParquetDataset(str(path), )
    parquet = data_set.read()

    df_raw = parquet.to_pandas()
    return df_raw


@lru_cache(1)
def load_processed_data(path: str) -> pd.DataFrame:
    df = load_data(path)
    logger.info(f'Removing duplicate locations; len:({len(df)})')
    _df = df.drop_duplicates(subset=['id', 'x', 'y'])

    actions = [
        ('Adding previous data calculations', aug.add_prev_data, False),
        ('Adding distance data calculations', aug.add_distance_data, False),
        ('Removing short series', aug.df_remove_short_series, True),
        ('Removing close points', aug.df_remove_close_points, True),
        ('Removing outliers', aug.remove_outliers, True),
        ('Smoothing data', aug.smooth, True),
    ]

    dfs = {'Original': _df}
    for title, action, plot_action in actions:
        logger.info(f'{title}; len:({len(_df)})')
        _df = action(_df)
        if plot_action:
            dfs[title] = _df

    logger.info(f'result data length:({len(_df)})')

    experiment = True
    if experiment:
        import data_viewer.trajectories_viewer as viewer
        h = 100000000000
        dfs = {k: d.head(h) for k, d in dfs.items()}
        viewer.plot_multi_data(dfs)

    return _df
