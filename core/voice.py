import ConfigParser
import logging
import pyvona

class Voice(object):
	instance = None
	def __init__(self):
		Voice.instance = self
		config = ConfigParser.RawConfigParser()
		config.read('pyvona.cfg')
		self.v = pyvona.create_voice(config.get('pyvona', 'accessKey'), config.get('pyvona', 'secretKey'))
		self.v.voice_name = config.get('pyvona', 'name')
		self.v.speech_rate = config.get('pyvona', 'rate')

	@staticmethod
	def getInstance():
		if Voice.instance is None:
			logging.debug('Create new instance')
			Voice.instance = Voice()
		return Voice.instance

	def say(self, str):
		self.v.speak(str)
