# raspberry-pi-assistant

Reginald is a Raspberri Pi assistant utilizing a pi and the Google Cloud Platform

Using a USB microphone the assistance is able to gather vocie recordings from around the raspberry pi

This is then sent to the Google Cloud Platform where it is processed by googles speech to text.

Using Google's Language Understanding to get the users intent from the utterance the result is then sent back to the
raspberry pi where it is processed and the correct dialog is run.

Any responses from the assistance are converted to speech with gTTS or similar text to speech software.

Using the sense hat the assistant is also able to retrieve information about its environment such as:

  - Temperature
  - Humidity
  - Pressure
  - Orientation
  - joystick movements
