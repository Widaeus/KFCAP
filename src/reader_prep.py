# Load dependencies
import os
import pandas as pd
import utils
from datetime import datetime

# Import raw data
def read_tabular_data(data_path):
    if data_path.endswith('.csv'):
      df = pd.read_csv(data_path)
    elif data_path.endswith('.xlsx'):
      df = pd.read_excel(data_path)
    else:
      raise ValueError("Unsupported file format")
    return df

# Conversion for OLO data
def convert_units_OLO(df):
    # Convert "hgb [mmol/L]" to "hgb [g/L]"
    if "hgb [mmol/L]" in df.columns:
        df["hgb [mmol/L]"] = pd.to_numeric(df["hgb [mmol/L]"], errors='coerce')
        df.rename(columns={"hgb [mmol/L]": "hgb [g/L]"}, inplace=True)
    
    # Convert "hgb [g/dL]" to "hgb [g/L]" by multiplying by 10
    if "hgb [g/dL]" in df.columns:
        df["hgb [g/dL]"] = pd.to_numeric(df["hgb [g/dL]"], errors='coerce') * 10
        df.rename(columns={"hgb [g/dL]": "hgb [g/L]"}, inplace=True)
    
    # Convert "hgb [g/L]" less than 20 to itself * 16
    if "hgb [g/L]" in df.columns:
        df["hgb [g/L]"] = df["hgb [g/L]"].apply(lambda x: x * 16 if x < 20 else x)
    
    # Convert "mchc [mmol/L]" to "mchc [g/L]"
    if "mchc [mmol/L]" in df.columns:
        df["mchc [mmol/L]"] = pd.to_numeric(df["mchc [mmol/L]"], errors='coerce')
        df.rename(columns={"mchc [mmol/L]": "mchc [g/L]"}, inplace=True)
    
    # Convert "mchc [g/dL]" to "mchc [g/L]" by multiplying by 10
    if "mchc [g/dL]" in df.columns:
        df["mchc [g/dL]"] = pd.to_numeric(df["mchc [g/dL]"], errors='coerce') * 10
        df.rename(columns={"mchc [g/dL]": "mchc [g/L]"}, inplace=True)
    
    # Convert "mchc [g/L]" less than 150 to itself * 16
    if "mchc [g/L]" in df.columns:
        df["mchc [g/L]"] = df["mchc [g/L]"].apply(lambda x: x * 16 if x < 150 else x)
    
    # Convert "mch [amol]" to "mch [pg]"
    if "mch [amol]" in df.columns:
        df["mch [amol]"] = pd.to_numeric(df["mch [amol]"], errors='coerce')
        df.rename(columns={"mch [amol]": "mch [pg]"}, inplace=True)
    
    # Convert "mch [pg]" greater than 100 to itself / 64.5
    if "mch [pg]" in df.columns:
        df["mch [pg]"] = df["mch [pg]"].apply(lambda x: x / 64.5 if x > 100 else x)
    
    # Convert "wbc [10^3/uL]" to "wbc [10^9/L]"
    if "wbc [10^3/uL]" in df.columns:
        df["wbc [10^3/uL]"] = pd.to_numeric(df["wbc [10^3/uL]"], errors='coerce')
        df.rename(columns={"wbc [10^3/uL]": "wbc [10^9/L]"}, inplace=True)
    
    # Convert "rbc [10^6/uL]" to "rbc [10^12/L]"
    if "rbc [10^6/uL]" in df.columns:
        df["rbc [10^6/uL]"] = pd.to_numeric(df["rbc [10^6/uL]"], errors='coerce')
        df.rename(columns={"rbc [10^6/uL]": "rbc [10^12/L]"}, inplace=True)
    
    # Convert "plt [10^3/uL]" to "plt [10^9/L]"
    if "plt [10^3/uL]" in df.columns:
        df["plt [10^3/uL]"] = pd.to_numeric(df["plt [10^3/uL]"], errors='coerce')
        df.rename(columns={"plt [10^3/uL]": "plt [10^9/L]"}, inplace=True)
    
    # Convert "hct [%]" to "hct [L/L]"
    if "hct [%]" in df.columns:
        df["hct [%]"] = pd.to_numeric(df["hct [%]"], errors='coerce') / 100
        df.rename(columns={"hct [%]": "hct [L/L]"}, inplace=True)
    
    # Conversions for Neutrophils, Lymphocytes, Monocytes, Eosinophils, and Basophils
    leukocyte_types = ["neut# ", "lymph# ", "mono# ", "eos# ", "baso# "]
    for leukocyte in leukocyte_types:
        full_colname = f"{leukocyte}[10^3/uL]"
        if full_colname in df.columns:
            df[full_colname] = pd.to_numeric(df[full_colname], errors='coerce')
            df.rename(columns={full_colname: f"{leukocyte}[10^9/L]"}, inplace=True)
    
    return df

# read_convert function
def read_convert(data_path):
    # Create a list of file paths for all .csv and .xlsx files in the specified directory
    file_list = [os.path.join(data_path, f) for f in os.listdir(data_path) if f.endswith(('.csv', '.xlsx'))]
    
    data_list = []
    differing_columns = {}
    
    # Read the first file and convert units
    first_df = read_tabular_data(file_list[0])
    first_df = convert_units_OLO(first_df)
    colnames_check = first_df.columns.tolist()
    
    for file in file_list:
        df = read_tabular_data(file)
        df = convert_units_OLO(df)
        differing_cols = set(df.columns.tolist()) - set(colnames_check)
        if differing_cols:
            differing_columns[file] = list(differing_cols)
        data_list.append(df)
    
    if differing_columns:
        with open("logs/differing_columns_log.txt", "w") as log_file:
            for file, cols in differing_columns.items():
                log_file.write(f"File: {file}\n")
                log_file.write(f"Differing columns: {', '.join(cols)}\n\n")
        raise ValueError("Column names differ across files. See differing_columns_log.txt for details.")
    
    # Convert all data to string
    data_list = [df.astype(str) for df in data_list]
    
    # Concatenate all dataframes
    concatenated_data = pd.concat(data_list, ignore_index=True)
    
    return concatenated_data

##########
# reading and conversion done
##########

# cleaning and fitting
def clean_olo(data, identifier, study="scapis_spectrum"):
    # Check if the study argument is valid
    if study not in ["mind", "scapis_spectrum"]:
        raise ValueError("The study argument must be either 'mind' or 'scapis_spectrum'.")

    # Remove tests (rows where 'sample_id' contains 'test', case-insensitive)
    data = data[~data['sample_id'].str.contains("test", case=False, na=False)]

    # Remove duplicate rows
    data = data.drop_duplicates()

    # Remove rows where 'reject_reason' is not NA
    data = data[data['reject_reason'].isna()]

    # Filter rows with correct scan_time formatting (HH:MM:SS)
    data = data[data['scan_time'].str.match(r"^\d{2}:\d{2}:\d{2}$", na=False)]

    # Convert columns to appropriate data types
    data = data.apply(pd.to_numeric, errors='ignore')

    # Function to count decimal places in a number
    def count_decimals(x):
        if pd.isna(x) or not isinstance(x, (int, float)):
            return 0
        x_str = str(x)
        if '.' in x_str:
            return len(x_str.split('.')[1])
        return 0

    # Process the data
    data['decimal_count'] = data['mch [pg]'].apply(count_decimals)
    data['flag_present'] = ~data['flags'].isna()

    # Sort by 'flag_present' and 'decimal_count', then keep the first row for each 'sample_id'
    data = (data.sort_values(by=['flag_present', 'decimal_count'], ascending=[False, False])
                .drop_duplicates(subset=['sample_id'])
                .drop(columns=['decimal_count', 'flag_present']))

    # Replace special characters in column names
    data.columns = data.columns.str.replace('%', '_percent').str.replace('#', '_number')

    # Drop specific columns
    data = data.drop(columns=['patient_id', 'patient_name', 'patient_date_of_birth', 'sex', 'age'])

    # Add a new column 'prover_complete' and set it to 1
    data['prover_complete'] = 1

    # Filter based on study type
    if study == "scapis_spectrum":
        data = data[~data['sample_id'].str.contains("MD", case=False, na=False)]
    elif study == "mind":
        data = data[data['sample_id'].str.contains("MD", case=False, na=False)]

    # Rename 'sample_id' to the identifier provided
    data = data.rename(columns={'sample_id': identifier})

    # Define new column names
    new_colnames = [
        "sample_type", "slide_id", "kit_id", "wbc_109l", "wbc_flagged",
        "rbc_1012l", "rbc_flagged", "plt_109l", "plt_flagged", "hgb_gl",
        "hgb_flagged", "hct_ll", "hct_flagged", "mcv_fl", "mcv_flagged",
        "rdw__percent", "rdw_flagged", "mch_pg", "mch_flagged", "mchc_gl",
        "mchc_flagged", "neut_percent__percent", "neut_percent_flagged",
        "neut_number_109l", "neut_number_flagged", "lymph_percent__percent",
        "lymph_percent_flagged", "lymph_number_109l", "lymph_number_flagged",
        "mono_percent__percent", "mono_percent_flagged", "mono_number_109l",
        "mono_number_flagged", "eos_percent__percent", "eos_percent_flagged",
        "eos_number_109l", "eos_number_flagged", "baso_percent__percent",
        "baso_percent_flagged", "baso_number_109l", "baso_number_flagged",
        "flags", "reject_reason", "scan_date", "scan_time", "sample_mode",
        "instrument_id", "scan_rev", "scan_tag", "export_rev", "config_rev",
        "config_tag", "operator_id", "operator_name", "demographic", "qc_status",
        "prover_complete"
    ]

    # Apply new column names (skipping the first column)
    data.columns.values[1:len(new_colnames) + 1] = new_colnames

    return data

# matching to REDcap
def match_to_redcap(data_olo, identifier, study="scapis_spectrum", api_token=None):
    # Check if the study argument is valid
    if study not in ["mind", "scapis_spectrum"]:
        raise ValueError("The study argument must be either 'mind' or 'scapis_spectrum'.")

    # Function to export REDCap data (this should be defined based on your API or database structure)
    data_redcap = utils.export_redcap_data(study, api_token)

    # Perform a left join on the REDCap data based on 'scapisstudynr'
    data_ammended = pd.merge(data_olo, data_redcap[[identifier, study]], how='left', on=identifier)

    return data_ammended

# writing to csv
def write_to_csv(df):
    # Construct the path to the 'data' folder
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current script's directory
    data_folder = os.path.join(script_dir, '..', 'data', 'processed')     # Navigate to the processed data folder

    # Ensure the 'data' folder exists
    os.makedirs(data_folder, exist_ok=True)

    # Get the current date for file naming
    today_date = datetime.today().strftime('%d_%m_%Y')

    # Create the full file path with the date appended to the filename
    file_path = os.path.join(data_folder, f'{today_date}.csv')

    # Export the DataFrame to CSV
    df.to_csv(file_path, index=False)

    print(f"Data successfully exported to {file_path}")
    
##########
# Combination function
##########

def reader_prep_csv(data_path, identifier, study, api_token=None):
    # Read and convert the data
    data_olo = read_convert(data_path)

    # Clean and fit the data
    data_cleaned = clean_olo(data_olo, identifier, study)

    # Match the data to REDCap
    data_matched = match_to_redcap(data_cleaned, identifier, study, api_token)
    
    # Write to csv
    write_to_csv(data_matched)

    pass