#!/usr/bin/env python3

from contextlib import closing
import configparser
import subprocess
import pyaudio
import boto3
import os

def make_recording():
    """Call bash script to record to 'request.wav'."""

    print("Listening...")
    subprocess.call("./record.sh")
    print("Done.")

def play_recording():
    """Call bash script to play 'request.wav'."""

    print("Playing 'recording.wav'...")
    subprocess.call("./play.sh")
    print("Done.")

def connect_to_lex():
    """Connect to Lex bot using AWS SDK."""

    config = configparser.ConfigParser()
    config.read('../../config.ini')

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

    make_recording()
    play_recording()
    
    print("Posting content to Reginald...")
    response = reginald.post_content(
        botAlias='demo',
        botName='Reginald',
        userId='VoiceRecognition',
        contentType='audio/l16; rate=16000; channels=1',
        inputStream=open('./request.wav', 'rb')
        )
    print("Done.")

    print("Playing response...")
    with closing(response["audioStream"]) as stream:
        with open("response.mp3", "wb") as file:
                    file.write(stream.read())
    os.system("mpg123 response.mp3")
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

    #Define reginald object.
    reginald = connect_to_lex()

    #Uncomment ONE:
    send_audio(reginald)
    #send_text(reginald)

main()