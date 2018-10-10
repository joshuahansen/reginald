#!/bin/bash

# Record for 3 seconds into file '~/reginald/audio/wavs/recording.wav'.
arecord --device=hw:1,0 --format S16_LE --rate 44100 -d 3 -c1 ~/reginald/audio/wavs/recording.wav
