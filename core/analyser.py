import scikits.audiolab, numpy, subprocess, sys, logging, audioop, time, pycurl, StringIO, os
from context import Context
from pocketsphinx import *
from os import path

class Analyser(object):

    MODELDIR = Context.getPocketsphinx('model.dir')
    HMM = Context.getPocketsphinx('hmm')
    THRESHOLD = int(Context.getAudio('threshold'))
    SEC2LISTEN = Context.getAudio('sec2listen')
    instance = None

    def __init__(self):
        # Create and configure decoder
        self.config = Decoder.default_config()
        self.config.set_string('-hmm', path.join(Analyser.MODELDIR, Analyser.HMM))
        self.config.set_string('-lm', path.join(Analyser.MODELDIR, Analyser.HMM, '%s.lm' % Context.getPocketsphinx('dict')))
        self.config.set_string('-dict', path.join(Analyser.MODELDIR, Analyser.HMM, '%s.dic' % Context.getPocketsphinx('dict')))
        self.config.set_string('-logfn', '/dev/null')
        self.decoder = Decoder(self.config)

    @staticmethod
    def getInstance():
        if Analyser.instance is None:
            Analyser.instance = Analyser()
        return Analyser.instance

    # function decode data using decoder, and return decoded string or None
    def decodeOffline(self, data):
        self.decoder.start_utt()
        self.decoder.process_raw(data, False, False)
        self.decoder.end_utt()
        if self.decoder.hyp() is not None and self.decoder.hyp().hypstr:
            return self.decoder.hyp().hypstr
        return None

    @staticmethod
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
