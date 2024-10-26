#!/bin/bash
pyinstaller --onefile --clean --name="KFCAP" --icon=icons/science.ico --noconsole --version-file=pyinstaller_version.txt src/main.py