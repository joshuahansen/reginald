#!/bin/bash

#Install system packages listed in 'pkg-requirements.txt' NOTE: WILL NOT PROMPT.
xargs -a ~/reginald/requirements/pkg-requirements.txt -r sudo apt-get install -y
