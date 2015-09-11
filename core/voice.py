import logging
import pyvona
from context import Context


class Voice(object):
    instance = None

    def __init__(self):
        self.v = pyvona.create_voice(Context.getPyvona('accessKey'), Context.getPyvona('secretKey'))
        self.v.voice_name = Context.getPyvona('name')
        self.v.speech_rate = Context.getPyvona('rate')

    @staticmethod
    def getInstance():
        if Voice.instance is None:
            Voice.instance = Voice()
        return Voice.instance

    def say(self, str):
        self.v.speak(str)
