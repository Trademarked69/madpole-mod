@echo off
set ver=1.3.3
rem build script for the distributable versions of tadpole
if not exist "venv\" (
    python -m venv venv
)
if not exist "venv\Lib\site-packages\PyInstaller" (
    venv\Scripts\python -m pip install pyinstaller
)
if not exist "venv\Lib\site-packages\PIL" (
    venv\Scripts\python -m pip install Pillow
)
if not exist "venv\Lib\site-packages\PyQt5" (
    venv\Scripts\python -m pip install PyQt5
)
pyinstaller madpole.py -n madpole_v0.1.exe -F --icon madpole.ico --clean --noconsole --version-file versioninfo --add-data="madpole.ico;." --add-data="README.md;."
