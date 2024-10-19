# KFCap Import Function

## Overview
This project provides an import function that takes a file in CSV or XLSX format and uses the REDCap API to import it into an electronic Case Report Form (eCRF) in REDCap. It further exposes this function as a GUI for easier end-user interaction.
It relies on PyCap for REDcap API integration.

## Features
- Supports CSV and XLSX file formats
- Utilizes REDCap API for data import
- Error handling and validation

## Requirements
- Python 3.13
- `pandas` library
- `requests` library

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
  pip install pandas requests
  ```

## Usage
1. Prepare your CSV or XLSX file with the required data.
2. Run the import function:
  ```python
  from kfcapimport import import_to_redcap

  file_path = 'path/to/your/file.csv'  # or 'file.xlsx'
  api_url = 'https://redcap.yourinstitution.edu/api/'
  api_token = 'YOUR_REDCAP_API_TOKEN'

  import_to_redcap(file_path, api_url, api_token)
  ```

## Example
```python
from kfcapimport import import_to_redcap

file_path = 'data/patient_data.csv'
api_url = 'https://redcap.yourinstitution.edu/api/'
api_token = 'YOUR_REDCAP_API_TOKEN'

import_to_redcap(file_path, api_url, api_token)
```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## Contact
For questions or support, please contact [jacob.widaeus@ki.se](mailto:jacob.widaeus@ki.se).