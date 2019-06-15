from pathlib import Path
import pytest
from yolo_detectors.configurations import yolo_detector_folders
from yolo_detectors.yolo_detector import YoloDetector

images_path = Path(__file__).parent / 'images'


@pytest.mark.parametrize('detector_arg', yolo_detector_folders.keys())
def test_single_detection(detector_arg):
    image_name = images_path / 'single_car.jpg'
    _test_detections(detector_arg, image_name, lambda count: count == 1, f'Expected to get 1 detection')


@pytest.mark.parametrize('detector_arg', yolo_detector_folders.keys())
def test_two_detections(detector_arg):
    image_name = images_path / 'two_cars.jpg'
    _test_detections(detector_arg, image_name, lambda count: count == 2, f'Expected to get 2 detection')


@pytest.mark.parametrize('detector_arg', yolo_detector_folders.keys())
def test_multi_detections(detector_arg):
    image_name = images_path / 'many_cars.jpg'
    min_expected_detections = 5
    _test_detections(detector_arg,
                     image_name,
                     lambda count: min_expected_detections <= count,
                     f'Expected to get at least {min_expected_detections} detection')


def _test_detections(detector_arg, image_name, predicate, error_message):
    detector = YoloDetector.factory(yolo=detector_arg)
    detections = detector.detect_from_image_path(image_name)
    car_detections = [detection for detection in detections if detection.label == 'car']
    # debug_draw_detections(detections, detector_arg, image_name)
    assert predicate(len(car_detections)), error_message


def debug_draw_detections(detections, detector_arg, image_name):
    from detection_handlers.detection_drawer import draw_detection
    import cv2
    image = cv2.imread(str(image_name))
    for d in detections:
        image = draw_detection(image, d)
    cv2.imshow(f'{detector_arg}: {image_name}', image)
    cv2.waitKey(0)


def main():
    test_multi_detections('v3')
    test_multi_detections('v3_tiny')
    test_multi_detections('v2')


if __name__ == '__main__':
    main()
