from collections import defaultdict

import pandas as pd
import argparse
from pathlib import Path
from typing import Union
import logging

from common.exceptions import ArgumentException
from settings import setup
import settings.all_cameras as cameras#import df_cameras, col_title, col_name, col_url
from pipelines.pipeline_director import get_auto_track_pipeline, get_debug_pipeline, get_road_roi_pipeline

from common.utils import init_log

logger = logging.getLogger(__name__)


def get_camera_info(camera_id: Union[int, str] = None):
    df_cameras = cameras.get_all_cameras()
    df_str = df_cameras[[cameras.col_name, cameras.col_title]].to_string()
    if camera_id is not None:
        df_match = df_cameras[df_cameras[cameras.col_name].str.lower() == str(camera_id).lower()]
        if len(df_match) == 1:
            s_data = df_match.iloc[0]
            return s_data
        elif Path(str(camera_id)).exists():
            # This allows specifying a file
            path = str(camera_id)
            title = Path(path).name.split('.')[0]
            data_factory = defaultdict(lambda:None)
            data_factory[cameras.col_name] = title
            data_factory[cameras.col_title] = title
            data_factory[cameras.col_url] = path
            s_data = pd.Series({c:data_factory[c] for c in df_cameras.columns})
            return s_data
        if not str(camera_id).isdigit():
            print(f'Valid cameras:\n{df_str}')
            raise ArgumentException(f'camera_id must be a valid folder or an integer '
                                    f'(got {type(camera_id).__name__} - {camera_id})')


    if camera_id is None:
        print(df_str)
        camera_id = input('please select a camera (integer)')
        if camera_id.isdigit():
            camera_id = int(camera_id)

        min_id = min(df_cameras.index)
        max_id = max(df_cameras.index)
        while not isinstance(camera_id, int) or camera_id < min_id or max_id < camera_id:
            camera_id = input(f'input must be a valid integer between {min_id} and {max_id}')
            if camera_id.isdigit():
                camera_id = int(camera_id)

    camera_id = int(camera_id)
    selected_row = df_cameras.loc[camera_id]
    msg = f'using camera: {selected_row[cameras.col_name]}'
    logger.debug(msg)

    return selected_row


def main(camera_id=None, yolo=None, save_folder=None):
    init_log()
    camera_data = get_camera_info(camera_id)

    # get_debug_pipeline
    # get_road_roi_pipeline
    # get_auto_track_pipeline

    # pipeline, observer = get_road_roi_pipeline(camera_data.url, yolo=yolo, title=camera_data.camera_name.lower(), save_folder=save_folder)
    pipeline, observer = get_auto_track_pipeline(url=camera_data.url, yolo=yolo, title=camera_data.camera_name.lower())

    logger.debug(f'subscribing observer ({observer}) to pipeline.')
    pipeline.subscribe(observer)


if __name__ == '__main__':
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-c', dest='camera', help='the id of camera to use or URL', required=False, default=None)
    parser.add_argument('-f', dest='folder', help='The folder to save stream to', required=False, default=None)
    parser.add_argument("-y", "--yolo", required=False, help="YOLO version or base folder to YOLO directory",
                        default='v3')

    parser.add_argument('-s', dest='setup', help='setup folder - e.g. Download weights', required=False, default=None,
                        action='store_true')
    args = parser.parse_args()

    if args.setup:
        setup.main()

    camera_id_arg = args.camera  # args.camera if args.camera >= 0 else None
    yolo_detector_arg = args.yolo
    save_folder_arg = args.folder
    main(camera_id=camera_id_arg, yolo=yolo_detector_arg, save_folder=save_folder_arg)
