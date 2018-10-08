#!/bin/bash

#Install npm packages listed in 'npm-requirements.txt'.
xargs -a ~/reginald/requirements/npm-requirements.txt -r npm install
