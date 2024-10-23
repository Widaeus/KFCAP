#!/bin/bash
pyinstaller --onefile --clean --name="KFC_REDcap_import" --icon=icons/science.ico --noconsole --version-file=pyinstaller_version.txt src/main.py