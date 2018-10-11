#!/usr/bin/env python3

from contextlib import closing
import configparser
import subprocess
import pyaudio
import boto3
import os
from sense_hat import SenseHat

directory = 'lex-audio/recordings/'

def make_recording():
    """Make a recording that stops once silence is detected."""

    print("Listening...")
    os.system('sox -d -t wavpcm -c 1 -b 16 -r 16000 -e signed-integer --endian little - silence 1 0 1% 5 0.3t 2% > {}request.wav'.format(directory))
    print("Done.")

def play_recording():
    """Play 'request.wav'."""

    print("Playing 'recording.mpg'...")
    os.system("aplay {}request.wav".format(directory))
    print("Done.")

def connect_to_lex():
    """Connect to Lex bot using AWS SDK."""

    config = configparser.ConfigParser()
    config.read('config.ini')

    if 'AWS' in config:
        ACCESS_KEY = config['AWS']['access_key']
        SECRET_KEY = config['AWS']['secret_key']

    print("Connecting to Reginald...")
    reginald = boto3.client(
        'lex-runtime',
        region_name='us-east-1',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY
        )
    print("Done.")

    return reginald

def send_audio(reginald):
    """Send audio to Lex bot."""

    # listern for recording
    make_recording()
    
    # debug recording playback
    # play_recording() 
    
    print("Posting content to Reginald...")
    response = reginald.post_content(
        botAlias='demo',
        botName='Reginald',
        userId='VoiceRecognition',
        contentType='audio/l16; rate=16000; channels=1',
        inputStream=open('{}request.wav'.format(directory), 'rb')
        )
    print("Done.")

    print("Playing response...")
    with closing(response["audioStream"]) as stream:
        with open("{}response.mp3".format(directory), "wb") as file:
                    file.write(stream.read())
    os.system("mpg123 {}response.mp3".format(directory))
    print("Done.")

    print(response)

def send_text(reginald):
    """Send text to Lex bot."""

    print("Posting text to Reginald...")
    #Change input here.
    input = "tell me a joke"
    response = reginald.post_text(
        botName='Reginald',
        botAlias='demo',
        userId='TextRecognition',
        inputText=input
        )
    print("Done.")

    print("Printing response...")
    print(response['message'])
    print("Done.")

    print(response)

def main():
    """Main function for module."""

    sense = SenseHat()
    #Define reginald object.
    reginald = connect_to_lex()
    
    run = True
    while run:

        for event in sense.stick.get_events():
            if event.action == "pressed":
                if event.direction == 'up':
                    run = False
                #Uncomment ONE:
                send_audio(reginald)
                #send_text(reginald)

main()
