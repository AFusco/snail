import abc

class StreamProcessor(object, metaclass=abc.ABCMeta):
    """StreamProcessor is the interface that stream processors must implement"""

    @abc.abstractmethod
    def process(self, input_stream):
        """ define the processing procedure.
        Use this function to define the way that midi must be processed and modified.
        Args:
            input_stream: the stream of notes to be processed
        Return:
            output_stream: the stream of processed notes
        """
        raise NotImplementedError(
            'This function must be user defined')