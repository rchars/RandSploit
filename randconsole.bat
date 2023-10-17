@echo off

set thascripts=%USERPROFILE%\.RandSploit\venv\Scripts
IF NOT EXIST "%thascripts%\activate.bat" (
	call setup.bat
)
IF NOT EXIST "%thascripts%\deactivate.bat" (
	call setup.bat
)
call %thascripts%\activate.bat
python -B randconsole.py
call %thascripts%\deactivate.bat
