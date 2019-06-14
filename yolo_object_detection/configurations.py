from pathlib import Path
from typing import Dict

yolo_detector_folders: Dict[str, Path] = {
    'v2': Path(__file__).parent / 'yolo-coco-v2',
    'v3': Path(__file__).parent / 'yolo-coco-v3',
    'v3_tiny': Path(__file__).parent / 'yolo-coco-v3-tiny',
}
