@echo off
python -m pip install --upgrade pip
python -m pip install virtualenv
python -m virtualenv venv
call venv\Scripts\activate.bat
pip install -r requirementsServer.txt
