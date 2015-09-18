from collections import deque


# Threshold tuner. Keep fixed size queue, and gives back average threshold plus margin
# In order to tune threshold all you need is to push 'silence' values into queue
class ThresholdTuner(object):
    def __init__(self, maxlen=5, defthreshold=880, margin=20):
        self.maxlen = maxlen
        self.th = int(defthreshold)
        self.deq = deque([self.th]*maxlen, maxlen=maxlen)
        self.margin = margin

    def push(self, item):
        self.deq.append(item)

    def getThresholed(self):
        sum = 0
        for i in self.deq:
            sum += i
        return (sum / self.maxlen) + self.margin
