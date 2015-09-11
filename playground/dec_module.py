import scikits.audiolab
import numpy
import subprocess, sys
import logging
from pocketsphinx import *
from os import path

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s\t(%(threadName)-10s) %(filename)s:%(lineno)d\t%(message)s')

MODELDIR = "/usr/local/share/pocketsphinx/model"
DATADIR = "/home/pi"

# function run 'arecord' console cmd for 'sec' seconds and gives back it's stdout
def listen(sec):
    reccmd = ["arecord", "-D", "plughw:0,0", "-f", "cd", "-c", "1", "-t", "wav", "-d", "%s"%sec, "-q", "-r", "16000"]
    proc = subprocess.Popen(reccmd, stdout=subprocess.PIPE)
    logging.info('Listening...')
    return proc.stdout.read()

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us/4986.lm'))
config.set_string('-dict', path.join(MODELDIR, 'en-us/en-us/4986.dic'))
config.set_string('-samprate', '48000')
decoder = Decoder(config)

data = listen(4)
logging.info('Processing...')

#data2file = numpy.frombuffer(data, dtype=numpy.int16)
#scikits.audiolab.wavwrite(data, 't2.wav', fs=16000)

decoder.start_utt()
decoder.process_raw(data, False, False)
decoder.end_utt()
if decoder.hyp() is not None:
    logging.info('Match: %s', decoder.hyp().hypstr)
else:
    logging.info('Nothing')

