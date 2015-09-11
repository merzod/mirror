# encoding: utf-8

import logging
from model import *
from weather import *
from master import *
from timer import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s\t(%(threadName)-10s) %(filename)s:%(lineno)d\t%(message)s')

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
mp2 = MasterPasiveProcessor(core)
mp.append(mp2)

core.appendPasive(mp)
core.append(mp)

# run command
# core.processCommand(Command.build('what is the weather today'))
# core.processCommand(Command.build('walle'))
# core.processCommand(Command.build('weater'))

while True:
	str = raw_input('>')
	core.processCommand(Command.build(str))
