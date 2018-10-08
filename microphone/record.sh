#!/bin/bash

arecord --device=hw:1,0 --format S16_LE --rate 44100 -c1 -d 5 recording.wav
