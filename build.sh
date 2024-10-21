#!/bin/bash
pyinstaller --onefile --clean --name="KFC_REDcap_import" --icon=icons/science.ico --noconsole --version-file=version.txt src/main.py