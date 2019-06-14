import pytest

from yolo_object_detection.configurations import yolo_detector_folders
from yolo_object_detection.yolo_config_folder import YoloFolder


@pytest.mark.parametrize('folder', [
    r'C:\Users\avitu\Documents\GitHub\Traffic\yolo_object_detection\yolo-coco-v3',
    r'C:\Users\avitu\Documents\GitHub\Traffic\yolo_object_detection\yolo-coco-v2',
    r'C:\Users\avitu\Documents\GitHub\Traffic\yolo_object_detection\yolo-coco-v3-tiny',
])
def test_folder_creation(folder):
    # Will throw exception upon failure
    yolo_folder = YoloFolder(folder)
    assert yolo_folder.folder.exists()


@pytest.mark.parametrize('path', yolo_detector_folders.values())
def test_detector_folder_exists(path):
    assert path.exists()
