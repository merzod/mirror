import numpy
import pyaudio
import analyse
import time
import threading
import sys
import Queue
from pocketsphinx import *
from os import path
import wave
import audioop
from scikits.samplerate import resample
import scikits.audiolab

pyaud = pyaudio.PyAudio()

size = 60
rate = 48000
frame = int(rate*0.05)
exit = False
q = Queue.Queue(size)
MODELDIR = "/usr/local/share/pocketsphinx/model"
DATADIR = "/home/pi"

config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us/4986.lm'))
config.set_string('-dict', path.join(MODELDIR, 'en-us/en-us/4986.dic'))
config.set_string('-logfn', '/dev/null')
config.set_string('-samprate', '%d' % rate)
decoder = Decoder(config)

stream = pyaud.open(
    format = pyaudio.paInt16,
    channels = 1, 
    rate = rate,
    input_device_index = 0,
    frames_per_buffer = frame,
    input = True)

def listen(stream, queue):
    try:
        while not exit:
            stream.start_stream()
            print('Listening...')
            for i in range(0,size):
                data = stream.read(frame)
                ar = numpy.fromstring(data, dtype=numpy.int16)
                data2 = resample(ar, (16000./48000.), 'linear')
                q.put(data2)
#                samps = numpy.fromstring(data, dtype=numpy.int16)
#                print (samps, q.qsize())
                rms = audioop.rms(data, 2)
                print rms
            stream.stop_stream()
            if exit:
                sys.exit()
            q.join()
    except IOError:
        print('ERROR!!!!')
        pass
    stream.stop_stream()
    stream.close()
    pyaud.terminate()
    print "----------------------------------------------------------------------------------------------------------------"

li = threading.Thread(target=listen, args = (stream, q))
li.start()

try:
    while True:
        while not q.full():
            time.sleep(1)
        print('Decoding...')
        wf = wave.open('t.wav', 'wb')
        wf.setnchannels(1)
        wf.setframerate(16000)
        wf.setsampwidth(pyaud.get_sample_size(pyaudio.paInt16))
        decoder.start_utt()
        a = numpy.array([])
        while not q.qsize() == 0:
            data = q.get()
            a = numpy.append(a, data)
            wf.writeframes(numpy.array_str(data))
            decoder.process_raw(data, False, False)
            if not q.qsize() == 0:
                q.task_done()
        decoder.end_utt()
        scikits.audiolab.wavwrite(a, 't2.wav', fs=16000, enc='pcm16')
        wf.close()
        if decoder.hyp() is not None:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Match: ', decoder.hyp().hypstr)
        else:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Not clear')
        q.task_done()
except(KeyboardInterrupt, SystemExit):
    print "exiting<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
    exit = True
    while not q.qsize() == 0:
        data = q.get()
        q.task_done()
    try:
        q.task_done()
    except ValueError:
        pass
    time.sleep(2)
    sys.exit()
