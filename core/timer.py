# encoding: utf-8

import threading
import logging
import time
from model import *
from voice import Voice

t = None
started = None
canceled = None


def action(processor):
    logging.info('Time!!!: %s' % processor)
    Voice.getInstance().say('Время вышло!')


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


class TimerProcessor(Processor):
    def __init__(self, tags={'таймер'}):
        super(TimerProcessor, self).__init__(tags)

    def processCommandByMyself(self, cmd):
        global t
        logging.debug('Checking timer state')
        if t is None:
            logging.info('Timer not run')
            Voice.getInstance().say('Таймер не запущен')
        elif t.isAlive():
            passed = time.time() - started
            logging.info('Timer is run for %d sec, left %d sec' % (t.interval, t.interval - passed))
            Voice.getInstance().say('Осталось %s' % secToString(t.interval - passed))
        else:
            if canceled is None:
                logging.info('Timer not run. Last was scheduled for %d sec, and finished %d sec ago' % (
                t.interval, time.time() - started - t.interval))
                Voice.getInstance().say('Таймер на %s завершился %s назад' % (
                secToString(t.interval), secToString(time.time() - started - t.interval)))
            else:
                logging.info('Timer not run. Last was scheduled for %d sec, and canceled %d sec ago' % (
                t.interval, time.time() - canceled))
                Voice.getInstance().say('Таймер на %s был отменен %s назад' % (
                secToString(t.interval), secToString(time.time() - canceled)))


class StartTimerProcessor(TimerProcessor):
    def __init__(self, tags={'секунд', 'минут'}):
        super(StartTimerProcessor, self).__init__(tags)

    def processCommandByMyself(self, cmd):
        global t
        global started
        global canceled
        preTag = None
        total = 0;
        for tag in cmd.tags:
            if tag.lower().startwith('минут') and preTag is not None:
                try:
                    min = int(preTag)
                except ValueError:
                    logging.error('Can\'t cast \'%s\' to int' % preTag)
                    return
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
            t = threading.Timer(total, action, args=[self])
            started = time.time()
            canceled = None
            t.start()
            logging.info('Start timer for %s' % secToString(total))
            Voice.getInstance().say('Таймер на %s запущен' % secToString(total))
        else:
            logging.debug('NOTHING')


class CancelTimerProcessor(TimerProcessor):
    def __init__(self, tags={'выключи', 'отмен'}):
        super(CancelTimerProcessor, self).__init__(tags)

    def processCommandByMyself(self, cmd):
        global t, canceled
        if t is not None and t.isAlive():
            logging.info('Cancel timer')
            t.cancel()
            canceled = time.time()
            Voice.getInstance().say('Таймер остановлен')
