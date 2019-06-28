from collections import defaultdict
import rx
from rx import operators as op

from builders.pipeline_builders import PipeLineBuilder





class PipelineDirector(object):
    """"""

    def __init__(self, builder: PipeLineBuilder):
        """"""
        super().__init__()
        self.builder = builder


    def __repr__(self):
        return super().__repr__()

    def build(self, source_func):
        # noinspection PyTypeChecker
        source = rx.create(source_func)
        processing_commands = self.builder.get_raw_data_processing_commands()
        augmentation_commands = self.builder.get_augmentation_commands()
        output_commands = self.builder.get_out_put_commands()

        pipeline = source
        for commands_list in [processing_commands, augmentation_commands, output_commands]:
            for cmd in commands_list:
                pipeline.pipe(cmd.execute)

        return pipeline



#
#
# def main():
#     from builders.visual_pipeline_builder import VisualPipelineBuilder
#     director = PipelineDirector(VisualPipelineBuilder())
#     director.build()
#     from common import layers
#
#     director._enum_to_commands(layers.Augmentation.STATISTICS)
#
#
# if __name__ == '__main__':
#     main()
