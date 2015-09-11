import scikits.audiolab
import numpy
import subprocess, os, sys

def listen():
    reccmd = ["arecord", "-D", "plughw:0,0", "-f", "cd", "-c", "1", "-t", "wav", "-d", "4", "-q", "-r", "16000"]
    proc = subprocess.Popen(reccmd, stdout=subprocess.PIPE)
    print 'listening...'
    return proc.stdout.read()

data = listen()
print 'decoding...'
data2 = numpy.frombuffer(data, dtype=numpy.int16)

scikits.audiolab.wavwrite(data2, 't2.wav', fs=16000)
