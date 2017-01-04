#!/usr/bin/python

import argparse
import logging as log
import os
import subprocess
import sys


from StreamProcessors.MainSP import *
from StreamProcessors.KeyChangerSP import *
from StreamProcessors.LadyCanazzaSP import *

from cache.MidiLoader import *

import music21 as m
	

def main():
	parser = argparse.ArgumentParser(prog='Snail')

	parser.add_argument('-if', '--input-file', type=argparse.FileType('r'),
	                   help='Set input directory or file', default='../midi/fe.mid')

	# Get verbosity from environment. If None, then set 3
	default_verbosity = os.getenv('SNAIL_DEFAULT_VERBOSITY', 3)


	git_desc = subprocess.check_output(['git', 'describe', '--always']).decode('utf-8')
	parser.add_argument('-V', '--version', action='version', 
						version='%(prog)s ' + git_desc)

	parser.add_argument('-v', '--verbosity', action='count',
	                    help='Increase level of verbosity',
	                    default=default_verbosity)



	args = parser.parse_args()

	if args.verbosity >= 3:
		logging_level = log.DEBUG
	elif args.verbosity >= 2:
		logging_level = log.INFO
	elif args.verbosity >= 1:
		logging_level = log.WARNING
	else:
		logging_level = log.ERROR

	#log.basicConfig(filename='example.log',level=logging_level)
	log.basicConfig(level=logging_level)

	log.info('Output verbosity: %s', args.verbosity)
	log.info('Input file: %s', args.input_file.name)

	s = m.stream.Stream()

	loader = MidiLoader()

	s = loader.load(os.path.abspath(args.input_file.name))


	# output = MainSP().then(LadyCanazzaSP(10)).then(KeyChangerSP(10)).process(s)
	log.debug('Guarda di che tipo è s: ')
	log.debug(s)
	output = MainSP().then(LadyCanazzaSP(delta=20)).process(s)

	mf = m.midi.translate.streamToMidiFile(output)
	mf.open('../midi/out.mid', 'wb')
	mf.write()
	mf.close()  



if __name__ == '__main__':
   main()
