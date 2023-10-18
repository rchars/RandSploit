@echo off


echo Starting setup...
set home=%USERPROFILE%\.RandSploit\venv
mkdir "%home%"
python -m venv "%home%"
call "%home%\Scripts\activate.bat"
pip install -r requirements.txt
call "%home%\Scripts\deactivate.bat"
echo All done.