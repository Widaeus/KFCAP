from reader_prep import reader_prep_csv, testing_no_clean
from utils import export_redcap_data, export_redcap_info
import getpass

data_path = 'data/raw'

testing_no_clean(data_path)