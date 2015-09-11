arecord -D plughw:0,0 -f cd -c 1 -t wav -d 0 -q -r 16000 | flac - -s -f --best --sample-rate 16000 -o test.flac
