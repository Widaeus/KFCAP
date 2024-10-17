import requests
import pandas as pd
import os
from datetime import datetime
import getpass

def export_redcap_data(api_token):
    """
    Exports REDCap data to a df.

    This function makes an API request to export REDCap data, converts the response to a pandas DataFrame,
    and returns it.

    Parameters:
    api_token (str): The API token for authentication.

    Example:
    export_redcap_data('your_api_token')
    """
    # Set up the parameters for the API request
    data = {
        'token': api_token,
        'content': 'record',
        'action': 'export',
        'format': 'json',
        'type': 'flat',
        'csvDelimiter': '',
        'rawOrLabel': 'raw',
        'rawOrLabelHeaders': 'raw',
        'exportCheckboxLabel': 'false',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': 'json'
    }
    
    # Make the API request
    response = requests.post('https://redcap.ki.se/api/', data=data)

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
    
def import_redcap_data(file_path, api_token, write='normal'):
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
    # Define the API URL
    api_url = 'https://redcap.ki.se/api/'

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
        
def export_redcap_info(api_token):
    """
    Exports REDCap info and prints it.

    This function makes an API request to export REDcap project data and prints it.

    Parameters:
    api_token (str): The API token for authentication.

    Example:
    export_redcap_info('your_api_token')
    """
    # Set up the parameters for the API request
    data = {
        'token': api_token,
        'content': 'project',
        'format': 'json',
        'returnFormat': 'json'
    }
    
    # Make the API request
    response = requests.post('https://redcap.ki.se/api/', data=data)

    # Check if the request was successful
    if response.status_code == 200:
        print("Export successful")
        try:
            return response.json()  # Parse and return the response as a dictionary
        except ValueError:
            raise RuntimeError("Failed to parse JSON response from REDCap")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None