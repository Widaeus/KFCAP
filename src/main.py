from reader_prep import reader_prep_csv
from utils import export_redcap_data

data_path = 'data/raw'
study = 'scapis_spectrum'

df = export_redcap_data()
print(df.head())