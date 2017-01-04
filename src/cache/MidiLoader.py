import logging as log
import music21 as m
import os.path
import pickle

#TODO: è tardi e la gestione degli errori è fatta abbastanza male

class MidiLoader(object):
	"""MidiLoader allows to save a native-format version of
	the stream associated with a midi file, in order to allow
	a faster loading instead of reprocessing"""

	cached_extension = '.snail'

	# def __init__(self, opts):
	# 	self.arg = arg

	def load(self, midi_path, check_cache=True, save_cache=True, silent=False):
		mf = m.midi.MidiFile()
		stream = None

		log.info('Loading file {}'.format(midi_path))

		if not os.path.isfile(midi_path):
			log.error('Specified midi file not found')
			raise IOError('File not found at {}'.format(midi_path))

		if check_cache:
			log.debug('Check cache flag is set')

			if self.has_cached_version(midi_path):
				log.info('Cached version found.')
				stream = self.load_cached_version(midi_path=midi_path)
			else:
				log.info('Cached version NOT found.')

			log.debug(stream)

			if stream != None:
				return stream

		stream = self.load_midi_file(midi_path=midi_path)

		log.debug(stream)


		if not silent and stream == None:
			log.error('Could not load specified midi file')
			raise IOError('File not found')

		if save_cache:
			log.debug('Saving cached version')
			self.save_cached_version(stream, midi_path=midi_path)

		return stream


	def has_cached_version(self, midi_path):
		cached_path = self.get_cached_path(midi_path)
		return os.path.isfile(cached_path)

	def load_midi_file(self, midi_path=''):
		try:
			log.debug('trying to open {}'.format(midi_path))
			mf = m.midi.MidiFile()
			mf.open(midi_path)
			mf.read()
			mf.close()
			return m.midi.translate.midiFileToStream(mf)
		except Exception as e:
			log.error('Could not load requested midi file: {}'.format(str(e)))
			return None


	def load_cached_version(self, cached_path='', midi_path=''):
		loaded_stream = None

		if cached_path == '' and midi_path != '':
			cached_path = self.get_cached_path(midi_path)

		try:
			loaded_stream = pickle.load(open(cached_path, 'rb'))
		except:
			loaded_stream = None

		return loaded_stream

	def save_cached_version(self, stream, midi_path='', cached_path=''):
		if cached_path == '' and midi_path != '':
			cached_path = self.get_cached_path(midi_path)

		try:
			pickle.dump(stream, open(cached_path, 'wb'))
		except:
			log.error('Could not save cached version of midi file')
			return None

	def get_cached_path(self, midi_path):
		return midi_path.rsplit('.', 1)[0] + self.cached_extension