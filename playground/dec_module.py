import scikits.audiolab, numpy, subprocess, sys, logging, audioop, time
from context import Context
from pocketsphinx import *
from os import path

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s\t(%(threadName)-10s) %(filename)s:%(lineno)d\t%(message)s')

MODELDIR = Context.getPocketsphinx('model.dir')
HMM = Context.getPocketsphinx('hmm')
THRESHOLD = int(Context.getPocketsphinx('threshold'))

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

def flac(data):
    flaccmd = ["flac", "-", "-s", "-f", "--best", "--sample-rate", Context.getPocketsphinx('rate'), "-o", "test.flac"]
    proc = subprocess.Popen(flaccmd, stdin=subprocess.PIPE)
    proc.communicate(data)

# function decode data using decoder, and return decoded string or None
def decodeOffline(decoder, data):
    decoder.start_utt()
    decoder.process_raw(data, False, False)
    decoder.end_utt()
    if decoder.hyp() is not None and decoder.hyp().hypstr:
        return decoder.hyp().hypstr
    return None

def decodeOnline(data):
    stt_url = 'https://www.google.com/speech-api/v2/recognize?output=json&lang=%s&key=%s' % (Context.getGoogle('locale'), Context.getGoogle('app.key'))

while True:
    logging.info('Listening...')
    data = listen(Context.getPocketsphinx('sec2listen'))
    rms = audioop.rms(data, 2)
    logging.debug('RMS: %d threshold: %d' % (rms, THRESHOLD))
    if rms > THRESHOLD:
        flac(data)
        str = decodeOffline(decoder, data)
        if str is not None and str:
            logging.info('You said: %s' % str)
        else:
            logging.debug('Noise...')
    time.sleep(2)


#data2file = numpy.frombuffer(data, dtype=numpy.int16)
#scikits.audiolab.wavwrite(data, 't2.wav', fs=16000)
