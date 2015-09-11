import ConfigParser

class Context(object):
    instance = None
    def __init__(self):
        self.config = ConfigParser.RawConfigParser()
        self.config.read('mirror.cfg')

    @staticmethod
    def getInstance():
        if Context.instance is None:
            Context.instance = Context()
        return Context.instance

    @staticmethod
    def get(section, key):
        return Context.getInstance().config.get(section, key)

    @staticmethod
    def getPocketsphinx(key):
        return Context.get('pocketsphinx', key)

    @staticmethod
    def getGoogle(key):
        return Context.get('google', key)

    @staticmethod
    def getAudio(key):
        return Context.get('audio', key)
