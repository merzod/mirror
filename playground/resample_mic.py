import pyaudio
import numpy
import scikits.audiolab
from scikits.samplerate import resample

p = pyaudio.PyAudio()
stream = p.open(
    format = pyaudio.paInt16,
    channels = 1,
    rate = 48000,
    input_device_index = 0,
    frames_per_buffer = int(48000*0.05),
    input = True
)

frames = []
for _ in range(0, 60):
    data = stream.read(int(48000*0.05))
    frames.append(numpy.frombuffer(data, dtype=numpy.int16))
    #frames.append(numpy.asarray(data))

data2 = numpy.hstack(frames)
stream.stop_stream()
stream.close()
p.terminate()
print data2

data3 = resample(data2, (16000./48000.), 'linear')
scikits.audiolab.wavwrite(data3, 't2.wav', fs=16000)
