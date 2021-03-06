#encoding:utf-8
import logging, subprocess, pyvona, threading
import pygame
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

    # Function says 'str' over pyvona
    def say(self, str):
        logging.debug('Say(online): %s' % str)
        self.v.speak(str)

    # Function says 'str' over espeak
    def sayOffline(self, str):
        logging.debug('Say(offline): %s' % str)
        subprocess.call('espeak "' + str + '"', shell=True)

    def sayCachedYes(self):
        self.playFile('../resources/yes.ogg')

    def sayCachedNotClear(self):
        self.playFile('../resources/not_clear.ogg')

    def sayCachedTimeout(self):
        self.playFile('../resources/timeout.ogg')

    def playFile(self, file):
        logging.debug('Say(cache): %s' % file)
        channel = pygame.mixer.Channel(5)
        sound = pygame.mixer.Sound(file)
        channel.play(sound)

    # Fay over pyvona
    def sayInThread(self, str):
        t = threading.Thread(target=self.say, args=(str,))
        t.start()

    # Function run 'arecord' console cmd for 'sec' seconds and gives back it's stdout
    def listen(self, sec):
        reccmd = ["arecord", "-D", "plughw:0,0", "-f", "cd", "-c", "1", "-t", "wav", "-d", "%d" % sec, "-q", "-r",
                  Context.getAudio('rate')]
        proc = subprocess.Popen(reccmd, stdout=subprocess.PIPE)
        return proc.stdout.read()
