# encoding: utf-8

import logging, subprocess, audioop, sys
from model import *
from weather import *
from master import *
from timer import *
from analyser import Analyser
from context import Context
from voice import Voice

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s\t(%(threadName)-10s) %(filename)s:%(lineno)d\t%(message)s')
logging.getLogger("requests").setLevel(logging.WARNING)

SEC2LISTEN = Context.getAudio('sec2listen')
THRESHOLD = int(Context.getAudio('threshold'))

core = Core()

# build active processors
proc = WeatherProcessor()
proc2 = TomorrowWeatherProcessor()
proc.append(proc2)
core.append(proc)

tp = TimerProcessor()
stp = StartTimerProcessor()
ctp = CancelTimerProcessor()
tp.append(stp)
tp.append(ctp)
core.append(tp)

# build pasive processor
mp = MasterProcessor(core)

core.appendPasive(mp)
# core.append(mp)

if len(sys.argv) == 2 and sys.argv[1]=='console':
    while True:
        str = raw_input('>')
        core.processCommand(Command.build(str, None))
else:
    while True:
        logging.info('Listening...')
        data = Voice.getInstance().listen(SEC2LISTEN)
        rms = audioop.rms(data, 2)
        logging.debug('RMS: %d threshold: %d' % (rms, THRESHOLD))
        if rms > THRESHOLD:
            result = ''
            if core.active:
                result = Analyser.decodeOnline(data)
                logging.info('You said(online): %s' % result)
            else:
                result = Analyser.getInstance().decodeOffline(data)
                logging.info('You said(offline): %s' % result)
            if result is not None and result:
                core.processCommand(Command.build(result, data))
            else:
                logging.debug('Noise...')
