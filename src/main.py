from reader_prep import reader_prep_csv
from utils import export_redcap_data, export_redcap_info
import getpass

data_path = 'data/raw'

# Prompt for the API token once
api_token = getpass.getpass("Enter your REDCap API token: ")

# Pass the token to the functions that need it
reader_prep_csv(data_path, api_token)