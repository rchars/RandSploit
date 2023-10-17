#!/bin/bash

echo "Starting setup..."
thascripts="$HOME/.RandSploit/venv"
python3 -m venv $thascripts
source "$thascripts/bin/activate"
pip install -r requirements.txt
deactivate
echo "All done."