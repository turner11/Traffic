from typing import List

from builders.pipeline_builders import PipeLineBuilder
from common.layers import RawDataProcessing, Augmentation, OutPut

DEFAULT_RAW_DATA_LAYERS = [RawDataProcessing.DETECTION, RawDataProcessing.TRACKING]
DEFAULT_AUGMENTATION_LAYERS = [Augmentation.DETECTION_DRAWING, Augmentation.STATISTICS]
DEFAULT_OUTPUT_LAYERS = [OutPut.SCREEN]


class RunTimePipelineBuilder(PipeLineBuilder):
    """"""

    def __init__(self,
                 raw_data_processing_commands: List[RawDataProcessing] = None,
                 augmentation_commands: List[Augmentation] = None,
                 out_put_commands: List[OutPut] = None):
        """"""

        super().__init__()
        self.raw_data_processing_commands = raw_data_processing_commands or DEFAULT_RAW_DATA_LAYERS
        self.augmentation_commands = augmentation_commands or DEFAULT_AUGMENTATION_LAYERS
        self.out_put_commands = out_put_commands or DEFAULT_OUTPUT_LAYERS

    def __repr__(self):
        return f'{self.__class__.__name__}({self.raw_data_processing_commands}, ' \
            f'{self.augmentation_commands}, ' \
            f'{self.out_put_commands})'



    def get_raw_data_processing_commands(self):
        types = [self._enum_to_commands(enum) for enum in self.raw_data_processing_commands]
        instances = [ctor() for ctor in types]
        return instances

    def get_out_put_commands(self):
        return [self._enum_to_commands(enum) for enum in self.raw_data_processing_commands]

    def get_augmentation_commands(self):
        pass
