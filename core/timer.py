# encoding: utf-8

import threading
import logging
import time
from model import *
from voice import Voice
import sys

sys.path.append('../hardware/')
import screen

SCREEN_UPDATE = 1

timer = None
started = None
canceled = None


# Once call the function after timer start and it will show time on the screen each sec.
# will auto stop when timeout
def tick():
    if timer is not None and timer.isAlive():
        threading.Timer(SCREEN_UPDATE, tick).start()
        passed = time.time() - started
        screen.ScreenWrapper.getInstance().write(secToFormat(timer.interval - passed), size=25)


# Callback for timer
def action(processor):
    logging.info('Time!!!: %s' % processor)
    screen.ScreenWrapper.getInstance().write('Timeout', size=30)
    Voice.getInstance().sayCachedTimeout()


# Time in seconds to human understandable string e.g. 3665 -> '1 hour 1 minute 5 seconds'
def secToString(sec):
    if sec >= 3600:
        s = sec / 3600
        str = '%d %s ' % (s, getName(s, 0))
        s = sec % 3600 / 60
        if s != 0:
            str += '%d %s ' % (s, getName(s, 1))
        s = sec % 3600 % 60
        if s != 0:
            str += '%d %s' % (s, getName(s, 2))
        return str
    elif sec >= 60:
        s = sec / 60
        str = '%d %s ' % (s, getName(s, 1))
        s = sec % 60
        if s != 0:
            str += '%d %s' % (s, getName(s, 2))
        return str
    else:
        return '%d %s' % (sec, getName(sec, 2))


# Time in seconds to formatted string e.g. 3665 -> '1:1:5'
def secToFormat(time):
    hour = time / 3600
    min = s = time % 3600 / 60
    sec = time % 3600 % 60
    return '%02d:%02d:%02d' % (hour, min, sec)


# Getting localized name of the time unit
def getName(val, type):
    if val % 10 == 1 and val != 11:
        if type == 0:
            return 'час'
        elif type == 1:
            return 'минуту'
        else:
            return 'секунду'
    elif val % 10 < 5 and val % 10 != 0 and val != 11 and val != 12 and val != 13 and val != 14:
        if type == 0:
            return 'часа'
        elif type == 1:
            return 'минуты'
        else:
            return 'секунды'
    else:
        if type == 0:
            return 'часов'
        elif type == 1:
            return 'минут'
        else:
            return 'секунд'


# Base time command processor. Processes timer state functionality
class TimerProcessor(Processor):
    def __init__(self, tags={'таймер'}):
        super(TimerProcessor, self).__init__(tags)

    def processCommandByMyself(self, cmd):
        global timer
        logging.debug('Checking timer state')
        if timer is None:
            logging.info('Timer not run')
            Voice.getInstance().say('Таймер не запущен')
        elif timer.isAlive():
            passed = time.time() - started
            logging.info('Timer is run for %d sec, left %d sec' % (timer.interval, timer.interval - passed))
            Voice.getInstance().say('Осталось %s' % secToString(timer.interval - passed))
        else:
            if canceled is None:
                logging.info('Timer not run. Last was scheduled for %d sec, and finished %d sec ago' % (
                    timer.interval, time.time() - started - timer.interval))
                screen.ScreenWrapper.getInstance().write(secToFormat(time.time() - started), size=25)
                Voice.getInstance().say('Таймер на %s завершился %s назад' % (
                    secToString(timer.interval), secToString(time.time() - started - timer.interval)))
            else:
                logging.info('Timer not run. Last was scheduled for %d sec, and canceled %d sec ago' % (
                    timer.interval, time.time() - canceled))
                Voice.getInstance().say('Таймер на %s был отменен %s назад' % (
                    secToString(timer.interval), secToString(time.time() - canceled)))


# Processes start timer command
class StartTimerProcessor(TimerProcessor):
    def __init__(self, tags={'секунд', 'минут', 'час'}):
        super(StartTimerProcessor, self).__init__(tags)

    def processCommandByMyself(self, cmd):
        global timer
        global started
        global canceled
        preTag = None
        total = 0
        for tag in cmd.tags:
            if tag.lower().startswith('час') and preTag is not None:
                try:
                    hour = int(preTag)
                except ValueError:
                    hour = 1
                logging.debug('Hour: %d' % hour)
                total += hour * 3600
            if tag.lower().startswith('минут') and preTag is not None:
                try:
                    min = int(preTag)
                except ValueError:
                    min = 1
                logging.debug('Min: %d' % min)
                total += min * 60
            elif tag.lower().startswith('секунд') and preTag is not None:
                try:
                    sec = int(preTag)
                except ValueError:
                    logging.error('Can\'t cast \'%s\' to int' % preTag)
                    return
                logging.debug('Sec: %d' % sec)
                total += sec
            preTag = tag
        if total > 0:
            if timer is not None and timer.isAlive():
                timer.cancel()
            timer = threading.Timer(total, action, args=[self])
            started = time.time()
            canceled = None
            timer.start()
            tick()
            logging.info('Start timer for %s' % secToString(total))
            Voice.getInstance().say('Таймер на %s запущен' % secToString(total))
        else:
            logging.debug('NOTHING')


# Processes stop cancel command
class CancelTimerProcessor(TimerProcessor):
    def __init__(self, tags={'выключи', 'отмен', 'остан'}):
        super(CancelTimerProcessor, self).__init__(tags)

    def processCommandByMyself(self, cmd):
        global timer, canceled
        if timer is not None and timer.isAlive():
            logging.info('Cancel timer')
            timer.cancel()
            canceled = time.time()
            Voice.getInstance().say('Таймер остановлен')
