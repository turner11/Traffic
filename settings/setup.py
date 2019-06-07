import logging
from pathlib import Path

import requests
from tqdm import tqdm

from settings.user_settings import data_root_path
from utils import init_log
from settings.constants import car_images_url

logger = logging.getLogger(__name__)

def download(url, dest):
    logger.debug(f'Downloading from "{url}" to {dest}')
    with open(dest, 'wb') as f:
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


def get_cars_data():

    # url = 'http://i3.ytimg.com/vi/J---aiyznGQ/mqdefault.jpg'
    root = Path(data_root_path)
    root.mkdir(parents=True, exist_ok=True)
    images_download_path = root / 'car_ims.tgz'
    if not images_download_path.exists():
        download(car_images_url, images_download_path)
    else:
        logger.info('car zip file already exists. Skipping download.')




def main():
    init_log()
    get_cars_data()



if __name__ == '__main__':
    main()
