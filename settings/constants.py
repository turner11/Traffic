from pathlib import Path
from settings.user_settings import data_root_path

car_images_url = 'http://imagenet.stanford.edu/internal/car196/car_ims.tgz'

train_cars_path = Path(data_root_path) / 'train'
test_cars_path = Path(data_root_path) / 'test'