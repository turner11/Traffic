import logging
from collections import namedtuple
from pathlib import Path
import requests
from tqdm import tqdm
from utils import init_log
from yolo_detectors.configurations import yolo_detector_folders
DownloadData = namedtuple('DownloadData', ['name', 'url', 'destination'])



logger = logging.getLogger(__name__)


def download(url, destination):
    with open(str(destination), 'wb') as f:
        response = requests.get(url, stream=True)

        # Retrieve HTTP meta-data
        logger.debug(f'status_code: {response.status_code}')
        logger.debug(f'content-type: {response.headers["content-type"]}')
        logger.debug(f'encoding: {response.encoding}')

        total_length = response.headers.get('content-length')

        if total_length is None:  # no content length header
            f.write(response.content)
        else:
            pbar = tqdm(total=int(total_length))  # Initialise
            for data in response.iter_content(chunk_size=4096):
                f.write(data)
                pbar.update(len(data))


def get_yolo_weights():
    # url = 'http://i3.ytimg.com/vi/J---aiyznGQ/mqdefault.jpg'

    v2_data = DownloadData('v2','https://pjreddie.com/media/files/yolov2.weights', yolo_detector_folders['v2']/'yolov2.weights')
    v3_data = DownloadData('v3', 'https://pjreddie.com/media/files/yolov3.weights', yolo_detector_folders['v3'] / 'yolov3.weights')
    v3_tiny_data = DownloadData('v3_tiny', 'https://pjreddie.com/media/files/yolov3-tiny.weights', yolo_detector_folders['v3_tiny'] / 'yolov3-tiny.weights')


    for download_data in [v2_data, v3_tiny_data, v3_data]:
        if not download_data.destination.exists():
            logger.info(f'Downloading {download_data.name}. From "{download_data.url}" to {download_data.destination}')
            download(download_data.url, download_data.destination)
        else:
            logger.info('car zip file already exists. Skipping download.')


def main():
    init_log()
    get_yolo_weights()


if __name__ == '__main__':
    main()
