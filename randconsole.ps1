$thascripts="$env:USERPROFILE\.RandSploit\venv\Scripts"
if(-not (Test-Path "${thascripts}\Activate.ps1" -PathType Leaf) -or -not (Test-Path "${thascripts}\deactivate.ps1" -PathType Leaf)) {
	Invoke-Expression -Command ".\setup.bat"
}
Invoke-Expression -Command "${thascripts}\Activate.ps1"
python -B randconsole.py
Invoke-Expression -Command "${thascripts}\deactivate.ps1"