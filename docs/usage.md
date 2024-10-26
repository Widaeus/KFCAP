# Usage Guide for KFCAPImport

## Table of Contents
1. [Basic Usage](#basic-usage)
3. [Configuration](#configuration)
4. [Troubleshooting](#troubleshooting)

### Basic Usage
The KFCAP import tool includes a GUI to import data from a CSV or XLSX file into a REDCap project at Kliniskt Forskningscentrum. The tool requires three inputs:
1. **Data path**: Path to the folder containing the data files for import.
2. **REDCap API token**: The API token for the specified REDCap project. Ensure the token is kept secure.
3. **Data form type**: The type of data to import (currently supports only OLO blood sample data).
<div style="margin-top: 20px;"></div>
The KFCAP alert handling tool takes a API token from REDCap project and outputs a list of all defined alert variables with the deviating values in **<span style="color:red;">red and bold</span>**. It features a scroll-like function to cycle through all the study ids with deviating values.

### Running the Application
You can run the application through the GUI by:
- **Creating an .exe file** using `PyInstaller` and `build.sh`, or
- Directly executing `main.py` from the command line:
  ```sh
  python main.py
  ```

### Configuration
All necessary dependencies are included when running the .exe. If running from `main.py`, ensure required libraries are installed by running:
```sh
pip install -r requirements.txt
```

### Troubleshooting
For any issues, refer to the core processing scripts:
- **Data reading and preparation**: `src/reader_prep.py`
- **REDCap API management**: `src/redcap.py`