#!/bin/bash

# Install system package requirements.
xargs -a ../requirements/pkg-requirements.txt -r sudo apt-get install -y
# Install npm package requirements.
xargs -a ../requirements/npm-requirements.txt -r npm install
# Install python package requirements.
pip install -r ../requirements/py3-requirements.txt
pip3 install -r ../requirements/py3-requirements.txt
# Copy .asoundrc to home directory.
cp ../requirements/.asoundrc ~/.asoundrc
# Remove existing snowboy directory.
rm -r ../snowboy
# Import snowboy package.
cd .. && mkdir snowboy && cd snowboy
wget https://s3-us-west-2.amazonaws.com/snowboy/snowboy-releases/rpi-arm-raspbian-8.0-1.2.0.tar.bz2
tar -xvf ./rpi-arm-raspbian-8.0-1.2.0.tar.bz2 && cd ../bash