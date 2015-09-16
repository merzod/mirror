# encoding: utf-8

from os import listdir
from os.path import isfile, join
from model import *
import random
import subprocess

player = None

class SongProcessor(Processor):
    def __init__(self, tags={'спой'}):
        super(SongProcessor, self).__init__(tags)

    def processCommandByMyself(self, cmd):
        path = '../resources/songs'
        files = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith('.mp3')]
        if len(files) > 0:
            id = random.randint(0, len(files)-1)
            name = files[id]
            global player
            player = subprocess.Popen(['mplayer', join(path, name)], stdin=subprocess.PIPE)

    @staticmethod
    def stopSinging():
        global player
        if player is not None:
            player.stdin.write('q')
            player = None





