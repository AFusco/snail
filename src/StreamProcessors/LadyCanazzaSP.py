import logging as log
import music21 as m
import random 

import pdb
from pprint import pprint

from .StreamProcessor import StreamProcessor

class LadyCanazzaSP(StreamProcessor):

	delta = 0

	def __init__(self, delta=0):
		if delta == 0 or delta > 100 or delta == 0:
			delta = random.uniform(0, 100)

		log.debug('init LCSP')
		log.debug('LCSP delta: {}'.format(delta))
		
		self.delta = delta

	def process(self, input_stream):
		for n in input_stream.flat.notes:
			try:
				# log.debug('Ricevo n: {}'.format(n))
				n.pitch.microtone = random.uniform(-self.delta, +self.delta)
				# log.debug(n.pitch.microtone.cents)
			except Exception:
				pass

		return input_stream