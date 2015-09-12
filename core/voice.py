import logging, subprocess, pyvona, threading
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

    # function says 'str' over pyvona
    def say(self, str):
        self.v.speak(str)

    def sayInThread(self, str):
        t = threading.Thread(target=self.say, args=(str,))
        t.start()

    # function run 'arecord' console cmd for 'sec' seconds and gives back it's stdout
    def listen(self, sec):
        reccmd = ["arecord", "-D", "plughw:0,0", "-f", "cd", "-c", "1", "-t", "wav", "-d", "%s"%sec, "-q", "-r", Context.getAudio('rate')]
        proc = subprocess.Popen(reccmd, stdout=subprocess.PIPE)
        return proc.stdout.read()
