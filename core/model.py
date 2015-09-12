import logging
from collections import deque
from analyser import Analyser


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
                if cmdTag.lower().startswith(myTag.lower()):
                    match += 1
        logging.debug('%d match between %s and %s' % (match, cmd, self))
        return match

    def processCommand(self, cmd):
        if super(Processor, self).processCommand(cmd) == 0:
            self.processCommandByMyself(cmd)

    def processCommandByMyself(self, cmd):
        raise NotImplementedError("Must be implemented")


class Core():
    def __init__(self):
        self.active = False
        self.activeProcessors = ChainProcessor()
        self.passiveProcessors = ChainProcessor()

    def processCommand(self, cmd):
        logging.info('Core active: \'%s\', processing: %s' % (self.active, cmd))

        # process command with either active or passive processors.
        if self.active:
            cmd = self.processCmdOnline(cmd)
            res = self.activeProcessors.processCommand(cmd)
            self.active = False
        else:
            res = self.passiveProcessors.processCommand(cmd)
            if res > 0 and len(cmd.tags) > 1:
                # In case of passive processing succeed - process with active also
                cmd = self.processCmdOnline(cmd)
                res2 = self.activeProcessors.processCommand(cmd)
                if res2 > 0:
                    # If active processing succeed - suspend Walle
                    self.active = False

        if res == 0:
            logging.warn('Failed to find any suitable processor for: %s' % cmd)

    def processCmdOnline(self, cmd):
        str = Analyser.decodeOnline(cmd.data)
        logging.info('You said(online): %s' % str)
        cmd.tags = str.split()
        return cmd

    def append(self, processor):
        self.activeProcessors.processors.append(processor)

    def appendPasive(self, processor):
        self.passiveProcessors.processors.append(processor)
