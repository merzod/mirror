import pyaudio
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
  dev = p.get_device_info_by_index(i)
  print((i,dev['name'],dev['maxInputChannels']))
  print (p.is_format_supported(16000.0, input_device=dev['index'], input_channels=dev['maxInputChannels'], input_format=pyaudio.paInt16))
