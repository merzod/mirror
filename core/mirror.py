# encoding: utf-8

import audioop
import sys

from weather import *
from timer import *
from context import Context
from song import *
from threshold import ThresholdTuner
import sys

sys.path.append('../hardware/')
import screen

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s\t(%(threadName)-10s) %(filename)s:%(lineno)d\t%(message)s')
logging.getLogger("requests").setLevel(logging.WARNING)

LISTEN = int(Context.getAudio('listen'))
MAX_SAMPLES = int(Context.getAudio('max.samples'))
threshold = ThresholdTuner(maxlen=int(Context.getAudio('threshold.samples')),
                           defthreshold=Context.getAudio('threshold'),
                           margin=int(Context.getAudio('threshold.margin')))

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

sp = SongProcessor()
sp.append(SongRepeatProcessor())
sp.append(SongStop())
core.append(sp)

screen.ScreenWrapper.getInstance().draw_walle_state()

try:
    if len(sys.argv) == 2 and sys.argv[1] == 'console':
        while True:
            str = raw_input('>')
            core.processCommand(Command.build(str, None))
    else:
        data = ''
        samples = 0
        while True:
            logging.info('Listening...')
            dt = Voice.getInstance().listen(LISTEN)
            th = threshold.getThresholed()
            rms = audioop.rms(dt, 2)
            logging.debug('RMS: %d threshold: %d' % (rms, th))
            if rms > th and samples < MAX_SAMPLES:
                logging.debug('Recording...')
                data += dt
                samples += 1
            elif len(data) > 0:
                data += dt  # append last sample (e.g. there is only one word at start of the sample, total RMS will
                # be bellow threshold, but still need to analyze it)
                logging.debug('Start analysing')
                result = Analyser.decodeOnline(data)
                logging.info('You said(online): %s' % result)
                if result:
                    core.processCommand(Command.build(result, data))
                else:
                    logging.debug('Noise...')
                    threshold.push(rms)
                data = ''
                samples = 0
            else:
                logging.debug('Silence...')
                threshold.push(rms)
except KeyboardInterrupt:
    del screen.ScreenWrapper.instance
