import logging
from collections import deque
from analyser import Analyser


# Command to process by the core
from voice import Voice


class Command(object):
    def __init__(self, tags, data):
        self.tags = tags
        self.data = data

    def __str__(self):
        return 'Cmd: %s' % self.tags

    @staticmethod
    def build(str, data):
        logging.debug('Building cmd from str: \'%s\'' % str)
        return Command(str.split(), data)


# Processor which contains the collection of the processors and tries to apply cmd to most suitable one
class ChainProcessor(object):
    def __init__(self):
        self.processors = deque()

    # list through processors and try to find best matched
    # if found - process the command with the processor
    def processCommand(self, cmd):
        logging.debug('Start chain processing: %s' % cmd)
        maxMatch = 0
        maxProcessor = None
        for processor in self.processors:
            iterMatch = processor.checkCommand(cmd)
            if iterMatch > maxMatch:
                maxMatch = iterMatch
                maxProcessor = processor
        if maxProcessor is not None:
            logging.info('Chain processing: %s with processor: %s' % (cmd, maxProcessor))
            maxProcessor.processCommand(cmd)
        return maxMatch

    def append(self, processor):
        self.processors.append(processor)


# Base processor, implements method checkCommand to check by own tags,
# but when processes the command, then try to process by children first (processCommand of ChainProcessor)
# if no suitable children - then process by it's own
class Processor(ChainProcessor):
    def __init__(self, tags):
        super(Processor, self).__init__()
        self.tags = tags

    def __str__(self):
        return 'Proc[%s]: %s, subProc: %d' % (type(self).__name__, self.tags, len(self.processors))

    def checkCommand(self, cmd):
        match = 0
        for myTag in self.tags:
            for cmdTag in cmd.tags:
                if cmdTag.decode('utf-8').lower().startswith(myTag.decode('utf-8').lower()):
                    match += 1
        logging.debug('%d match between %s and %s' % (match, cmd, self))
        return match

    def processCommand(self, cmd):
        if super(Processor, self).processCommand(cmd) == 0:
            self.processCommandByMyself(cmd)

    def processCommandByMyself(self, cmd):
        raise NotImplementedError("Must be implemented")


# Processing core. Has state and 2 processing queues (depending on sate)
class Core():
    def __init__(self):
        self.active = False
        self.activeProcessors = ChainProcessor()
        self.passiveProcessors = ChainProcessor()

    def processCommand(self, cmd):
        logging.info('Core active: \'%s\', processing: %s' % (self.active, cmd))

        # process command with either active or passive processors.
        if self.active:
            res = self.activeProcessors.processCommand(cmd)
            if res == 0:
                Voice.getInstance().sayCachedNotClear()
            logging.info('Suspend Walle')
            self.active = False
        else:
            res = self.passiveProcessors.processCommand(cmd)

        if res == 0:
            logging.warn('Failed to find any suitable processor for: %s' % cmd)

    def append(self, processor):
        self.activeProcessors.processors.append(processor)

    def appendPasive(self, processor):
        self.passiveProcessors.processors.append(processor)
