import os
from reader_prep import reader_prep_csv
from utils import export_redcap_data, export_redcap_info
import getpass
import pandas as pd
from redcap.methods import records

# Define the URL and API token for your REDCap project
REDCAP_API_URL = 'https://redcap.example.com/api/'
API_TOKEN = 'your_api_token'

# Initialize the REDCap project
project = Project(REDCAP_API_URL, API_TOKEN)

# Export records
records = project.export_records(format='json')

# Convert the exported records to a DataFrame
df = pd.DataFrame(records)

# Display the DataFrame
print(df)