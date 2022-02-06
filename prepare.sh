#!/bin/bash

# Download list of words
curl https://raw.githubusercontent.com/dwyl/english-words/master/words.txt -o data/words-raw.txt

# Clean it
source env/bin/activate
python prepare.py
deactivate