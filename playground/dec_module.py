import scikits.audiolab, numpy, subprocess, sys, logging, audioop, time, pycurl, StringIO, os
from context import Context
from pocketsphinx import *
from os import path

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s\t(%(threadName)-10s) %(filename)s:%(lineno)d\t%(message)s')
MODELDIR = Context.getPocketsphinx('model.dir')
HMM = Context.getPocketsphinx('hmm')
THRESHOLD = int(Context.getAudio('threshold'))
SEC2LISTEN = Context.getAudio('sec2listen')

# Create and configure decoder
config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, HMM))
config.set_string('-lm', path.join(MODELDIR, HMM, '%s.lm' % Context.getPocketsphinx('dict')))
config.set_string('-dict', path.join(MODELDIR, HMM, '%s.dic' % Context.getPocketsphinx('dict')))
config.set_string('-logfn', '/dev/null')
decoder = Decoder(config)

# function run 'arecord' console cmd for 'sec' seconds and gives back it's stdout
def listen(sec):
    reccmd = ["arecord", "-D", "plughw:0,0", "-f", "cd", "-c", "1", "-t", "wav", "-d", "%s"%sec, "-q", "-r", Context.getAudio('rate')]
    proc = subprocess.Popen(reccmd, stdout=subprocess.PIPE)
    return proc.stdout.read()

def chainListen():
    frames = ''
    for _ in range(1, 4):
        data = listen(1)
        frames += data
        rms = audioop.rms(data, 2)
        if rms < THRESHOLD:
            break
    return frames


# function decode data using decoder, and return decoded string or None
def decodeOffline(decoder, data):
    decoder.start_utt()
    decoder.process_raw(data, False, False)
    decoder.end_utt()
    if decoder.hyp() is not None and decoder.hyp().hypstr:
        return decoder.hyp().hypstr
    return None

# decode wav input data using google recognize API, returns recognized string
def decodeOnline(data):
    stt_url = 'https://www.google.com/speech-api/v2/recognize?output=json&lang=%s&key=%s' % (Context.getGoogle('locale'), Context.getGoogle('app.key'))
    fout = StringIO.StringIO()

    c = pycurl.Curl()
    c.setopt(pycurl.VERBOSE, 0)
    c.setopt(pycurl.URL, stt_url)
    c.setopt(pycurl.WRITEFUNCTION, fout.write)
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.HTTPHEADER, ['Content-Type: audio/l16; rate=%s' % Context.getAudio('rate')])
    c.setopt(pycurl.POSTFIELDSIZE, len(data))
    c.setopt(pycurl.READFUNCTION, StringIO.StringIO(data).read)
    c.perform()

    response_data = fout.getvalue()
    logging.debug(response_data)

    start_loc = response_data.find("transcript")
    temp_str = response_data[start_loc + 13:]
    end_loc = temp_str.find("\"")
    final_result = temp_str[:end_loc]
    c.close()
    return final_result

while True:
    logging.info('Listening...')
    #data = listen(SEC2LISTEN)
    data = chainListen()
    rms = audioop.rms(data, 2)
    logging.debug('RMS: %d threshold: %d' % (rms, THRESHOLD))
    if rms > THRESHOLD:
        # onlineRes = decodeOnline(data)
        # logging.info('You said(online): %s' % onlineRes)
        offlineRes = decodeOffline(decoder, data)
        if offlineRes is not None and offlineRes:
            logging.info('You said(offline): %s' % offlineRes)
        else:
            logging.debug('Noise...')


#data2file = numpy.frombuffer(data, dtype=numpy.int16)
#scikits.audiolab.wavwrite(data, 't2.wav', fs=16000)
