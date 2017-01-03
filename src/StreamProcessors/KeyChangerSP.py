import logging as log

from .StreamProcessor import StreamProcessor

class KeyChangerSP(StreamProcessor):
	""" KeyChangerSP is a StreamProcessor which transposes of a given key_offset 
		each note of a stream 
	"""

	key_offset = 0

	def __init__(self, key_offset):
		self.key_offset = key_offset

	def process(self, input_stream):
		return input_stream.transpose(self.key_offset)
