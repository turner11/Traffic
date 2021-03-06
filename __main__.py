import argparse
from collections import namedtuple
from pathlib import Path
from typing import Union
import pandas as pd
import logging

from builders.auto_track_builder import AutoTrackBuilder
from builders.debug_builder import DebugBuilder
from builders.road_detector_builder import RoadDetectorBuilder
from common.exceptions import ArgumentException
from settings import setup
from settings.all_cameras import data as cameras_dict
from builders.pipeline_director import PipelineDirector

from common.utils import init_log

logger = logging.getLogger(__name__)


def get_url(camera_id: Union[int, str] = None):
    if camera_id is not None:
        if Path(str(camera_id)).exists():
            # This allows specifying a file
            path = str(camera_id)
            return path, path
        if not str(camera_id).isdigit():
            raise ArgumentException(f'camera_id must be a valid path or an integer '
                                    f'(got {type(camera_id).__name__} - {camera_id})')

    col_index, col_name, col_title, col_url = 'index', 'name', 'title', 'player_url_web'
    CameraInfo = namedtuple('CameraInfo', [col_index, col_name, col_title, col_url])
    all_cameras = [CameraInfo(i, d['name'], d['title'], d['player_url_web']) for i, d in enumerate(cameras_dict)]

    df = pd.DataFrame(all_cameras).set_index(col_index)

    if camera_id is None:
        print(df[[col_name, col_title]].to_string())
        camera_id = input('please select a camera (integer)')
        if camera_id.isdigit():
            camera_id = int(camera_id)

        min_id = min(df.index)
        max_id = max(df.index)
        while not isinstance(camera_id, int) or camera_id < min_id or max_id < camera_id:
            camera_id = input(f'input must be a valid integer between {min_id} and {max_id}')
            if camera_id.isdigit():
                camera_id = int(camera_id)

    camera_id = int(camera_id)
    selected_row = df.loc[camera_id]
    msg = f'using camera: {selected_row[col_name]}'
    logger.debug(msg)

    url = selected_row[col_url]
    title = selected_row[col_name]
    return url, title


def main(camera_id=None, yolo=None, save_folder=None):
    init_log()
    url, title = get_url(camera_id)

    # builder = DebugBuilder(yolo=yolo)
    builder = AutoTrackBuilder(yolo=yolo)
    # builder = RoadDetectorBuilder(yolo=yolo)
    director = PipelineDirector(builder)
    pipeline, observer = director.build(url, title.lower(), save_folder=save_folder)

    pipeline.subscribe(observer)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-c', dest='camera', help='the id of camera to use or URL', required=False, default=None)
    parser.add_argument('-f', dest='folder', help='The folder to save stream to', required=False, default=None)
    parser.add_argument("-y", "--yolo", required=False, help="YOLO version or base path to YOLO directory",
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
