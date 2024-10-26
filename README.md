# KFCAP

## Overview
This project facilitates the import and viewing of REDCap projects within Kliniskt Forskningscentrum at Danderyd Hospital.
<div style="margin-top: 20px;"></div>
The import functionality supports CSV and XLSX file formats, leveraging the REDCap API to import data into an electronic Case Report Form (eCRF) in REDCap. Additionally, it provides a user-friendly GUI for easier interaction.
It extensively uses **PyCap** for REDCap API integration.
<div style="margin-top: 20px;"></div>
The alert handling feature, as of version `1.0.2`, is currently available for the "SCAPIS2spectrum" and "MIND" studies. It utilizes a modified version of PyCap to check alert parameters, identify study records that triggered alerts, and present them in the GUI for an overview.

## Features
- Import
  - Supports CSV and XLSX file formats
  - Utilizes REDCap API for data import
  - GUI for easier end-user interaction
- Alert handling
  - REDCap API prompt for values and study record naming
  - GUI for viewing and scrolling between IDs
  - Deviating values marked in **<span style="color:red;">red and bold</span>**.

## Requirements
Please see the [requirements.txt](requirements.txt) file for a list of required libraries. For .exe creation PyInstaller is required.

## Installation
1. Clone the repository:
  ```sh
  git clone https://github.com/widaeus/KFCAP.git
  ```
2. Navigate to the project directory:
  ```sh
  cd KFCAP
  ```
3. Install the required libraries:
  ```sh
  pip install -r requirements.txt
  ```

## Usage
For GUI:
Create .exe file with Pyinstaller using build.sh, or run main.py.
GUI takes three inputs: data path to folder with files to be improted, REDcap API token and what form of data to be imported. As of version `1.0.2` only OLO blood sample data is supported.

Remember to keep API token safe and not share it or write it in code.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## Contact
For questions or support, please contact [jacob.widaeus@ki.se](mailto:jacob.widaeus@ki.se).
