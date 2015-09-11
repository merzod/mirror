import scikits.audiolab
import numpy
from scikits.samplerate import resample
from matplotlib import pyplot as plt

data, fs, enc = scikits.audiolab.wavread('test.wav')
data2 = numpy.asarray(data)
data3 = resample(data2, (16000./48000.), 'linear')
scikits.audiolab.wavwrite(data3, 't2.wav', fs=16000)#, enc=enc)

plt.plot(data2)
plt.savefig('a.png', dpi=100)
