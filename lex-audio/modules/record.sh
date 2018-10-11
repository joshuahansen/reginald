#!/bin/bash

# Record for 3 seconds into file 'request.mpg'.
arecord --device=hw:1,0 --format S16_LE --rate 44100 -d 3 -c1 request.mpg
