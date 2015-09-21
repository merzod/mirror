# encoding: utf-8

from os import listdir
from os.path import isfile, join
from model import *
import random
import subprocess
import logging

player = None
last = 0


class SongProcessor(Processor):
    def __init__(self, tags={'спой'}):
        super(SongProcessor, self).__init__(tags)
        self.path = '../resources/songs'

    def processCommandByMyself(self, cmd):
        files = self.getSongs()
        if len(files) > 0:
            global last
            id = last
            while id == last:
                id = random.randint(0, len(files) - 1)
            last = id
            self.play(files[id])
        else:
            logging.warn('There is no songs in the folder %s' % self.path)

    def getSongs(self):
        return [f for f in listdir(self.path) if isfile(join(self.path, f)) and f.endswith('.mp3')]

    def play(self, name):
        global player
        player = subprocess.Popen(['mplayer', join(self.path, name)], stdin=subprocess.PIPE)

    @staticmethod
    def stopSinging():
        global player
        if player is not None:
            try:
                player.stdin.write('q')
            except IOError:
                pass
            player = None


class SongRepeatProcessor(SongProcessor):
    def __init__(self, tags={'повтор', 'еще', 'ещё'}):
        super(SongRepeatProcessor, self).__init__(tags)

    def processCommandByMyself(self, cmd):
        global last
        files = self.getSongs()
        if len(files) > last:
            self.play(files[last])
        else:
            logging.warn('Found files in folder less then last play id')
