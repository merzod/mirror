#!/bin/bash
# parameter 1 : file name, containg flac encoded voiuce recording
 
echo Sending FLAC encoded Sound File to Google:
url='https://www.google.com/speech-api/v2/recognize?output=json&lang=ru&key=AIzaSyDQqnWCFH41MwIHN5iVUDeoD13piO6sAeg'
curl -X POST --data-binary @$1 --header 'Content-Type: audio/x-flac; rate=16000;' $url
echo '..all done'
