import logging as log

from .StreamProcessor import StreamProcessor

class MainSP(StreamProcessor):
	""" MainSP is used to chain multiple StreamProcessors, in order to create 
		a pipeline of processors. 
	"""

	chain = []


	def then(self, next):
		"""
        Adds a processor to the pipeline. It is not executed.
        Args:
        	next: StreamProcessor to be added to the pipeline
        Returns:
            self
        """
		self.chain.append(next)
		return self

	def process(self, input_stream):
		"""
		Executes all pipelined processors in order of addition.
		Args:
			input_stream: the input m21 stream
		Returns:
			output_stream: the final processed m21 stream
		"""
		output_stream = input_stream

    	# TODO: check if chain is empty
		if len(self.chain) == 0:
			log.warning('No operations chained. Echoing input.')
			return output_stream

		for sp in self.chain:
			output_stream = sp.process(output_stream)

		return output_stream