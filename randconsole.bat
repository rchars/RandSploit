@echo off


call venv\Scripts\activate.bat
python -B randconsole.py
call venv\Scripts\deactivate.bat
