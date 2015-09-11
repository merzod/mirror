import scikits.audiolab
import numpy
import subprocess, sys
import logging
from pocketsphinx import *
from os import path
import audioop


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s\t(%(threadName)-10s) %(filename)s:%(lineno)d\t%(message)s')

MODELDIR = "/usr/local/share/pocketsphinx/model"
DATADIR = "/home/pi"
SEC = 4
THRESHOLD = 600

# function run 'arecord' console cmd for 'sec' seconds and gives back it's stdout
def listen(sec):
    reccmd = ["arecord", "-D", "plughw:0,0", "-f", "cd", "-c", "1", "-t", "wav", "-d", "%s"%sec, "-q", "-r", "16000"]
    proc = subprocess.Popen(reccmd, stdout=subprocess.PIPE)
    return proc.stdout.read()

# function decode data using decoder, and return decoded string or None
def process(decoder, data):
    decoder.start_utt()
    decoder.process_raw(data, False, False)
    decoder.end_utt()
    if decoder.hyp() is not None and decoder.hyp().hypstr:
        return decoder.hyp().hypstr
    return None


# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us/1722.lm'))
config.set_string('-dict', path.join(MODELDIR, 'en-us/en-us/1722.dic'))
config.set_string('-samprate', '48000')
config.set_string('-logfn', '/dev/null')
decoder = Decoder(config)

while True:
    logging.info('Listening...')
    data = listen(SEC)
    rms = audioop.rms(data, 2)
    logging.debug('RMS: %d' % rms)
    if rms > THRESHOLD:
        str = process(decoder, data)
        logging.info('Match: %s' % str)


#data2file = numpy.frombuffer(data, dtype=numpy.int16)
#scikits.audiolab.wavwrite(data, 't2.wav', fs=16000)
