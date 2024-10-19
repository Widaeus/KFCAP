# KFCap Import Function

## Overview
This project provides an import function that takes a file in CSV or XLSX format and uses the REDCap API to import it into an electronic Case Report Form (eCRF) in REDCap. It further exposes this function as a GUI for easier end-user interaction.
It relies on PyCap for REDcap API integration.

## Features
- Supports CSV and XLSX file formats
- Utilizes REDCap API for data import
- GUI for easier end-user interaction

## Requirements
Please see the [requirements.txt](requirements.txt) file for a list of required libraries. For .exe creation PyInstaller is required.

## Installation
1. Clone the repository:
  ```sh
  git clone https://github.com/yourusername/KFCapimport.git
  ```
2. Navigate to the project directory:
  ```sh
  cd KFCapimport
  ```
3. Install the required libraries:
  ```sh
  pip install -r requirements.txt
  ```

## Usage
For GUI:
Create .exe file with PyInstaller or run main.py.
GUI takes three inputs: data path to folder with files to be improted, REDcap API token and what form of data to be imported. As of version 1.0.0 only OLO blood sample data is supported.

Remember to keep API token safe and not share it or write it in code.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## Contact
For questions or support, please contact [jacob.widaeus@ki.se](mailto:jacob.widaeus@ki.se).