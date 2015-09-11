from pocketsphinx import *
from os import path
import pyaudio
import time

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
DEV = 0
RATE = 48000
CHUNK = int(RATE*0.05)

MODELDIR = "/usr/local/share/pocketsphinx/model"
DATADIR = "/home/pi"

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us/3023.lm'))
config.set_string('-dict', path.join(MODELDIR, 'en-us/en-us/3023.dic'))
decoder = Decoder(config)

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
		input_device_index=DEV,
                frames_per_buffer=CHUNK)

print ("READY....")

# Decode streaming data.
decoder.start_utt()
utt_started = False
while True:
    data = stream.read(CHUNK)
#    time.sleep (0.100)
    decoder.process_raw(data, False, False)
    in_speech = decoder.get_in_speech()
    
    if in_speech and not utt_started:
        #silence -> speech transition,
        #let user know that he is heard
        print("Started...\n")
        utt_started = True
        
    if not in_speech and utt_started:
        #speech -> silence transition,
        #time to start new utterance
        decoder.end_utt()
        # Retrieve hypothesis.
        hypothesis = decoder.hyp()
        if hypothesis is not None:
            print ('Best hypothesis: ', hypothesis.best_score, hypothesis.hypstr)
        utt_started = False
        decoder.start_utt()
        #Indicate listening for next utterance
        print ("NEXT....")

#close micraphone
stream.stop_stream()
stream.close()
p.terminate()
print("Ended...")
