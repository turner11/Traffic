import logging
import shutil
import sys

import cv2
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path
from typing import Union, List
from commands.payload import Payload
from observers.abstract_observer import ObserverBase

logger = logging.getLogger(__name__)


class SaveTabularDataObserver(ObserverBase):

    def __init__(self, folder, prompt=True):
        """"""
        super(SaveTabularDataObserver).__init__()
        self.prompt = prompt
        self.folder = Path(folder)
        self.current_payload = None

    def on_next(self, payload: Payload):
        self.current_payload = payload

    def on_error(self, error):
        self.save_data()
        super().on_error(error)

    def on_completed(self):
        self.save_data()
        super().on_completed()

    def save_data(self):
        dfs = self.current_payload.session_data_frames
        dfs = {name: df for name, df in dfs.items() if df is not None and len(df)}
        should_save = len(dfs) and not self.prompt or self.should_save_payload()
        if not should_save:
            return

        self.folder.mkdir(exist_ok=True, parents=True)

        for name, df in dfs.items():
            if len(df):
                path = str(self.folder / name) + '.prqt'
                partition_col = None  # 'label'
                self.save_parquet(df, path, partition_col=partition_col)

        for name, img in self.current_payload.images.items():
            path = str(self.folder / name) + '.jpg'
            cv2.imwrite(path, img)



    @staticmethod
    def save_parquet(df: pd.DataFrame, path: Union[str, Path], partition_col: Union[List[str], str, None] = None):
        logger.debug(f'saving parquet to:\n{path}')
        path = Path(path)
        if path.exists():
            try:
                shutil.rmtree(path)
            except Exception as ex:
                logger.warning(f'Failed to delete parquet: {ex}')

        # noinspection PyArgumentList
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

    def should_save_payload(self, default="yes"):
        valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
        question = f'Should I save the data? ({str(self.folder)})'

        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while True:
            sys.stdout.write(f'{question} {prompt}')
            choice = input().lower()
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes'/'no' (or 'y'/'n').\n")
