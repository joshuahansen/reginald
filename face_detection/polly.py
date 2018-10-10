import boto3
from contextlib import closing
import configparser
import random


def speech_synthesize(name):
    config = configparser.ConfigParser()
    config.read('config.ini')

    if 'AWS' in config:
            ACCESS_KEY = config['AWS']['access_key']
            SECRET_KEY = config['AWS']['secret_key']

    polly = boto3.client(
            'polly',
            region_name='us-east-1',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY
            )
    greetings = ['Hello {}', 'Hi {}', 'Welcome {}', 'Greetings {}', 'I can see you {}']

    text = random.choice(greetings).format(name)
    voice_id = 'Matthew'
    language_code = 'en-AU'
    text_type = 'text'
    output_format = 'mp3'

    response = polly.synthesize_speech(
            OutputFormat=output_format,
            Text=text,
            TextType=text_type,
            VoiceId=voice_id,
            LanguageCode=language_code
            )
    
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            output = "face_detection/polly-response.mp3"

            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                # Could not write to file, exit gracefully
                print(error)
                sys.exit(-1)

