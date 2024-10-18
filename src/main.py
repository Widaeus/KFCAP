import os
import pandas as pd
from redcap.project import Project

# Define the API token as environment variable as
# set REDCAP_API_TOKEN="api token"

# Define the URL and API token for your REDCap project
REDCAP_API_URL = 'https://redcap.ki.se/api/'
API_TOKEN = os.getenv('REDCAP_API_TOKEN_mind')

if not API_TOKEN:
    raise ValueError("API token not found. Please set the REDCAP_API_TOKEN environment variable.")

# Initialize the REDCap project
project = Project(REDCAP_API_URL, API_TOKEN)

# Export records
records = project.export_records(format_type='json')

# Convert the exported records to a DataFrame
df = pd.DataFrame(records)

# Display the DataFrame
print(df)