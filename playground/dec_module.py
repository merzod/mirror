import scikits.audiolab, numpy, subprocess, sys, logging, audioop
from context import Context
from pocketsphinx import *
from os import path

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s\t(%(threadName)-10s) %(filename)s:%(lineno)d\t%(message)s')

MODELDIR = Context.getPocketsphinx('model.dir')
HMM = Context.getPocketsphinx('hmm')

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, HMM))
config.set_string('-lm', path.join(MODELDIR, HMM, '%s.lm' % Context.getPocketsphinx('dict')))
config.set_string('-dict', path.join(MODELDIR, HMM, '%s.dic' % Context.getPocketsphinx('dict')))
config.set_string('-logfn', '/dev/null')
decoder = Decoder(config)

# function run 'arecord' console cmd for 'sec' seconds and gives back it's stdout
def listen(sec):
    reccmd = ["arecord", "-D", "plughw:0,0", "-f", "cd", "-c", "1", "-t", "wav", "-d", "%s"%sec, "-q", "-r", Context.getPocketsphinx('rate')]
    proc = subprocess.Popen(reccmd, stdout=subprocess.PIPE)
    return proc.stdout.read()

# function decode data using decoder, and return decoded string or None
def decodeOffline(decoder, data):
    decoder.start_utt()
    decoder.process_raw(data, False, False)
    decoder.end_utt()
    if decoder.hyp() is not None and decoder.hyp().hypstr:
        return decoder.hyp().hypstr
    return None

while True:
    logging.info('Listening...')
    data = listen(int(Context.getPocketsphinx('sec2listen')))
    rms = audioop.rms(data, 2)
    logging.debug('RMS: %d' % rms)
    if rms > int(Context.getPocketsphinx('threshold')):
        str = decodeOffline(decoder, data)
        logging.info('Match: %s' % str)


#data2file = numpy.frombuffer(data, dtype=numpy.int16)
#scikits.audiolab.wavwrite(data, 't2.wav', fs=16000)
