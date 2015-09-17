# encoding: utf-8

import logging, subprocess, audioop, sys
from model import *
from weather import *
from master import *
from timer import *
from analyser import Analyser
from context import Context
from voice import Voice
from song import SongProcessor
from threshold import ThresholdTuner

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s\t(%(threadName)-10s) %(filename)s:%(lineno)d\t%(message)s')
logging.getLogger("requests").setLevel(logging.WARNING)

ACTIVE_LISTEN = Context.getAudio('active.listen')
SUSPEND_LISTEN = Context.getAudio('suspend.listen')
threshold = ThresholdTuner(maxlen=Context.getAudio('threshold.samples'),
                           defthreshold=Context.getAudio('threshold'))

core = Core()

# build active processors
proc = WeatherProcessor()
proc.append(TomorrowWeatherProcessor())
proc.append(NowWeatherProcessor())
core.append(proc)

tp = TimerProcessor()
tp.append(StartTimerProcessor())
tp.append(CancelTimerProcessor())
core.append(tp)

core.append(SongProcessor())

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
        if core.active:
            data = Voice.getInstance().listen(ACTIVE_LISTEN)
        else:
            data = Voice.getInstance().listen(SUSPEND_LISTEN)

        th = threshold.getThresholed()
        rms = audioop.rms(data, 2)
        logging.debug('RMS: %d threshold: %d' % (rms, th))
        if rms > th:
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
                threshold.push(rms)
        else:
            threshold.push(rms)
