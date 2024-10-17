import requests
import pandas as pd
import os
from datetime import datetime
import getpass

def export_redcap_data(output_dir, study, api_token=None):
    """
    Exports REDCap data to a CSV file.

    This function makes an API request to export REDCap data, converts the response to a pandas DataFrame,
    and saves it as a CSV file in the specified output directory. The CSV file is named with the current date
    and the study name as a prefix.

    Parameters:
    api_token (str): The API token for authentication.
    output_dir (str): The directory where the CSV file will be saved.
    study (str): The name of the study to be used as a prefix for the export file's name.

    Example:
    export_redcap_data('your_api_token', 'C:\\path\\to\\output\\directory', 'study')
    """
    # Prompt the user for the API key if not provided
    if api_token is None:
        api_token = getpass.getpass("Enter your REDCap API token: ")

    # Set up the parameters for the API request
    data = {
        'token': api_token,
        'content': 'record',
        'format': 'json',
        'type': 'flat',
        'rawOrLabel': 'raw',
        'rawOrLabelHeaders': 'raw',
        'exportCheckboxLabel': 'false',
        'returnFormat': 'json'
    }

    # Make the API request
    response = requests.post('https://redcap.ki.se/redcap/api/', data=data)

    # Check if the request was successful
    if response.status_code == 200:
        print("Export successful")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return

    # Convert the API response to a pandas DataFrame
    df = pd.DataFrame(response.json())

    return df
    
def import_redcap_data(file_path, api_token=None, write='normal'):
    """
    Imports REDCap data from a CSV file to REDCap via API.

    This function reads the content of a specified CSV file, prepares the payload for the API request,
    and sends the data to the REDCap API. The API URL is predefined.

    Parameters:
    file_path (str): The path to the CSV file to be imported.
    api_token (str): The API token for authentication.
    write (str): The behavior for handling existing records. Options are 'normal' (append) or 'overwrite'.

    Example:
    import_scapis_data('C:/path/to/your/csv_file.csv', 'your_api_token')
    """
    # Prompt the user for the API key if not provided
    if api_token is None:
        api_token = getpass.getpass("Enter your REDCap API token: ")

    # Define the API URL
    api_url = 'https://redcap.ki.se/redcap/api/'

    # Read the CSV file content as a string
    with open(file_path, 'r') as file:
        csv_data = file.read()

    # Prepare the payload for the API request
    payload = {
        'token': api_token,
        'content': 'record',
        'format': 'csv',
        'type': 'flat',
        'overwriteBehavior': write,
        'data': csv_data,
        'returnContent': 'count',
        'returnFormat': 'json'
    }

    # Make the API request
    response = requests.post(api_url, data=payload)

    # Check the response from REDCap
    if response.status_code == 200:
        print('Data import was successful.')
        print('Response:', response.json())
    else:
        print('Data import failed.')
        print('Response:', response.text)