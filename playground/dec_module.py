import scikits.audiolab
import numpy
import subprocess, os, sys

def listen():
    reccmd = "ls -la"
    proc = subprocess.Popen(reccmd, stdout=subprocess.PIPE)
    return proc.stdout.read()

data = listen()
#data = numpy.asarray(listen())
scikits.audiolab.wavwrite(data, 't2.wav', fs=16000)