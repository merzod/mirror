from collections import deque

class ThresholdTuner(object):
    def __init__(self, maxlen=5, defthreshold=880):
        self.maxlen = maxlen
        self.th = int(defthreshold)
        self.deq = deque([self.th]*maxlen, maxlen=maxlen)

    def push(self, item):
        self.deq.append(item)

    def getThresholed(self):
        sum = 0
        for i in self.deq:
            sum += i
        return (sum / self.maxlen) + 20
