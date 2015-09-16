# encoding: utf-8

import logging
from model import *
from voice import Voice
import song


# Master processor, activates Walle
class MasterProcessor(Processor):
    def __init__(self, core, tags={'walle'}):
        super(MasterProcessor, self).__init__(tags)
        self.core = core

    def processCommandByMyself(self, cmd):
        if not self.core.active:
            logging.info('Activate Walle')
            self.core.active = True
            song.SongProcessor.stopSinging()
            # Voice.getInstance().say('Да?')
            Voice.getInstance().sayCachedYes()
