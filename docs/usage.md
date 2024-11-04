# Usage Guide for KFCAP

## Table of Contents
1. [Basic Usage](#basic-usage)
2. [Main Menu](#main-menu)
3. [Data Import](#data-import)
4. [Alert Handling](#alert-handling)
5. [Letter Generation](#letter-generation)
### Basic Usage
The KFCAP analysis and import tool streamlines integration with the REDCap API, allowing for easy viewing of alerts, data import, and generation of letters with embedded QR codes. For installation instructions, please refer to the README documentation.

### Main Menu
To use the application, a valid API token for REDCap must be provided. If the API token is valid and connects to an eCRF, a valid label will be displayed in <span style="color:green">green</span>. <br>
Once the API token is entered, a session manager will activate and remain active for the duration of the session (as long as the window is open). The session will terminate when you close the window. <br>
For security reasons, the API token or data will not be saved. Upon validation of the API token, three options will be available: Data Import, Alert Handling, and Letter Generation.

### Data Import
The Data Import function is only usable when the eCRF has variables exactly matching those contained within the desired csv/xlsx file to import. If using certain presets "OLO data" and "Echocardiographic data", the function will apply certain conversions and reformatting to enable smooth import. 

### Alert Handling
The Alert Handling function is designed to easily identify records with deviating values in the alerts, in conjunction with other deviating values. <br>
It is compatible only with "simple" alerts; complex AND, OR, IF statements are not supported.

Example: if you have set an alert in REDCap to warn when the variable `blood_pressure_systolic` is higher than 180, download the alert CSV file containing the alerts and insert it into the "Alert Conditions File". <br>
The program will identify the different alerts within the file. Select the relevant alerts you want to view. You may choose more than one, but compatibility issues may arise, so it is recommended to select one at a time. <br>
When you click run, a window pane will display all the variables contained within the alert, their values, and their references within the alert. The deviating variable and value will be highlighted in red. You can navigate through the records to view each deviating record's individual values. <br>
After exiting Alert Handling, the alerts will reset.


### Letter Generation
The Letter Generation function is currently not live, and thus should not be used.

It is meant to create letters where an embedded QR code will be generated based on a record-specific survey instrument from REDcap, aswell as adress info for sending letters. It will also take selection as input (a list of record_ids for generation)