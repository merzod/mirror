# encoding: utf-8

from os import listdir
from os.path import isfile, join
from model import *
import random
from voice import Voice

class SongProcessor(Processor):
    def __init__(self, tags={'спой'}):
        super(SongProcessor, self).__init__(tags)

    def processCommandByMyself(self, cmd):
        path = '../resources/songs'
        files = [f for f in listdir(path) if isfile(join(path, f)) and f.endswith('.mp3')]
        if len(files) > 0:
            id = random.randint(0, len(files))
            name = files[id]
            Voice.getInstance().playFile(name)




