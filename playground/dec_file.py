from pocketsphinx import *
from os import path
import pyaudio
import time
import numpy
import wave
import sys

MODELDIR = "/usr/local/share/pocketsphinx/model"
DATADIR = "/home/pi"

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us/4986.lm'))
config.set_string('-dict', path.join(MODELDIR, 'en-us/en-us/4986.dic'))
config.set_string('-samprate', '48000')

decoder = Decoder(config)
decoder.start_utt()
name = 'test.wav'
if len(sys.argv) == 2:
    name = sys.argv[1]
print 'NAME: %s' % name
s = open(name)
decoder.process_raw(s.read(), False, False)
decoder.end_utt()
print ("Match: ", decoder.hyp().hypstr)
print('Seg: ', [seg.word for seg in decoder.seg()])
