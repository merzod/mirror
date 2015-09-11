# encoding: utf-8

import logging
from model import *
from voice import Voice

class MasterProcessor(Processor):
	def __init__(self, core, tags={'walle'}):
		super(MasterProcessor, self).__init__(tags)
		self.core = core

	def processCommandByMyself(self, cmd):
		if not self.core.active:
			logging.info('Activate Walle')
			self.core.active = True
			Voice.getInstance().say('Привет')

class MasterPasiveProcessor(MasterProcessor):
	def __init__(self, core, tags={'bye'}):
		super(MasterPasiveProcessor, self).__init__(core, tags)

	def processCommandByMyself(self, cmd):
		if self.core.active:
			logging.info('Standby Walle')
			self.core.active = False		
			Voice.getInstance().say('Пока')
