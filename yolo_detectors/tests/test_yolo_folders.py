import pytest

from yolo_detectors.configurations import yolo_detector_folders
from yolo_detectors.yolo_config_folder import YoloFolder


@pytest.mark.parametrize('folder',yolo_detector_folders.values())
def test_folder_creation(folder):
    # Will throw exception upon failure
    yolo_folder = YoloFolder(folder)
    assert yolo_folder.folder.exists()


@pytest.mark.parametrize('path', yolo_detector_folders.values())
def test_detector_folder_exists(path):
    assert path.exists()