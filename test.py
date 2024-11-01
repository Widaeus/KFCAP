import pandas as pd

# Set display options to show the entire content of the 'alert-condition' column
pd.set_option('display.max_colwidth', None)

# Load CSV file into a DataFrame
df = pd.read_csv('C:/Users/jacoes/OneDrive - Karolinska Institutet/Dokument/Projekt/KFC/KFCAP/data/raw/SCAPIS2Spectrum_Alerts_2024-11-01.csv')

# Print the 'alert-condition' column
print(df['alert-condition'])