#!/bin/bash


thascripts="$HOME/.RandSploit/venv/bin/activate"
if [ ! -e "$thascripts" ]; then
	./setup.sh
fi
source "$thascripts"
python3 -B randconsole.py
deactivate
