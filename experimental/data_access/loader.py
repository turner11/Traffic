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
    logger.debug(f'Adding previous data calculations')
    df_with_prev = aug.add_prev_data(df)

    logger.debug(f'Adding distance data calculations')
    df_with_distance = aug.add_distance_data(df_with_prev)

    logger.debug(f'Removing outliers')
    df_clean = aug.remove_outliers(df_with_distance)
    logger.debug(f'Data size with / without outliers: {(len(df_with_distance), len(df_clean))}')

    # logger.debug(f'Smoothing data')
    # df_smooth = aug.smooth(df_clean)

    logger.debug(f'Removing short series')
    df_processed = aug.df_remove_short_series(df_clean)
    logger.debug(f'Data size before / after short removal: {(len(df_clean), len(df_processed))}')

    return df_processed
