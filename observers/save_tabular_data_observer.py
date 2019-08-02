import logging
import shutil
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
from typing import Union, List
from commands.payload import Payload
from observers.abstract_observer import ObserverBase

logger = logging.getLogger(__name__)


class SaveTabularDataObserver(ObserverBase):

    def __init__(self, path):
        """"""
        super(SaveTabularDataObserver).__init__()
        self.path = path
        self.df = None

    def on_next(self, payload: Payload):
        df = payload.dfs.get('detections', pd.DataFrame()).drop_duplicates()
        if len(df):
            self.df = df

    def on_error(self, error):
        self.save_data()
        super().on_error(error)

    def on_completed(self):
        self.save_data()
        super().on_completed()

    def save_data(self):
        self.save_parquet(self.df, self.path, partition_col='label')

    @staticmethod
    def save_parquet(df: pd.DataFrame, path: Union[str, Path], partition_col: Union[List[str], str, None] = None):
        logger.debug(f'saving parquet to:\n{path}')
        path = Path(path)
        if path.exists():
            try:
                shutil.rmtree(path)
            except Exception as ex:
                logger.warning(f'Failed to delete parquet: {ex}')

        table = pa.Table.from_pandas(df)

        if isinstance(partition_col, str):
            partition_col = [partition_col]
        return pq.write_to_dataset(table, root_path=str(path), partition_cols=partition_col, )

    @staticmethod
    def load_parquet(path, columns: Union[List[str], None] = None, filters: Union[List[str], None] = None):
        logger.debug(f'loading parquet from:\n{path}')
        data_set = pq.ParquetDataset(str(path), filters=filters)

        parquet = data_set.read(columns=columns)
        # try:
        # except ArrowInvalid as e:
        #     raise NoDataException(str(e)) from e

        return parquet
