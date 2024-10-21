# Usage Guide for KFCAPImport

## Table of Contents
1. [Basic Usage](#basic-usage)
2. [GUI](#GUI)
3. [Configuration](#configuration)
4. [Troubleshooting](#troubleshooting)

## Basic usage
The KFCAPImport tool is a GUI guided tool that can be used to import data from a CSV or XLSX file into a REDCap project. The tool requires a REDCap API token, a folder of data files, and a data form type as input. The data file should be in CSV or XLSX format and should contain the data to be imported into REDCap.

## GUI
The GUI is a simple interface that guides the user through the process of importing data into REDCap. It runs from main.py or from the .exe created by build.sh.

The GUI requires the following inputs:
- Data path: The path to the folder containing the data files to be imported.
- REDCap API token: The API token for the REDCap project.
- Data form type: The type of data form to be imported. As of version 1.0.0, only OLO blood sample data is supported.

Remember to keep the API token safe and not share it or write it in code.

## Configuration
When running the .exe all dependencies are included in the build. If running from main.py, the required libraries can be installed using the following command:
```sh
pip install -r requirements.txt
```

## Troubleshooting
If you encounter issues, the main reading, converting and modifying code is found in src/reader_prep.py. The REDcap API OOP code is found in src/redcap.