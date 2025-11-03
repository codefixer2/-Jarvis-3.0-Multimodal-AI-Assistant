@echo off
echo Installing Jarvis 3.0 dependencies...
py -3.12 -m pip install --upgrade pip
py -3.12 -m pip install -r requirements.txt
echo Done. If any errors show, check the logs above.
pause
