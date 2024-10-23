# Load dependencies
import os
import pandas as pd
from datetime import datetime
import re

def read_tabular_data(data_path):
    """
    Reads tabular data from a given file path.
    
    Parameters:
    data_path (str): The path to the data file. Supported formats are .csv and .xlsx.
    
    Returns:
    DataFrame: A pandas DataFrame containing the data.
    
    Raises:
    ValueError: If the file format is not supported.
    """
    if data_path.endswith('.csv'):
      df = pd.read_csv(data_path)
    elif data_path.endswith('.xlsx'):
      df = pd.read_excel(data_path)
    else:
      raise ValueError("Unsupported file format")
    return df

def convert_units_OLO(df):
    """
    Converts units for OLO data in the given DataFrame.
    
    Parameters:
    df (DataFrame): The pandas DataFrame containing OLO data.
    
    Returns:
    DataFrame: The DataFrame with converted units.
    """
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
            
    # Apply rounding rules
    if "plt [10^9/L]" in df.columns:
        df["plt [10^9/L]"] = df["plt [10^9/L]"].round(0).astype('Int64')
    
    if "hgb [g/L]" in df.columns:
        df["hgb [g/L]"] = df["hgb [g/L]"].round(0).astype('Int64')
    
    if "hct [L/L]" in df.columns:
        df["hct [L/L]"] = df["hct [L/L]"].round(2)
    
    if "mch [pg]" in df.columns:
        df["mch [pg]"] = df["mch [pg]"].round(1)
    
    if "mchc [g/L]" in df.columns:
        df["mchc [g/L]"] = df["mchc [g/L]"].round(0).astype('Int64')
    
    return df

def read_convert(data_path):
    """
    Reads and converts OLO data from a given file path.
    Relies on convert_units_OLO in module reader_prep.
    
    Parameters:
    data_path (str): The path to the OLO data file.
    
    Returns:
    DataFrame: A pandas DataFrame containing the converted OLO data.
    """
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

def clean_olo(data, project):
    """
    Cleans and fits OLO data for a given project.
    Assumes that REDcap has the appropriate column names for OLO data.
    
    Parameters:
    data (DataFrame): The pandas DataFrame containing OLO data.
    project (str): The project identifier, from PyCap.
    
    Returns:
    DataFrame: The cleaned and fitted OLO data.
    """
    # Fetch project info
    project_info = project.export_project_info()
    
    # Remove tests (rows where 'sample_id' contains 'test', case-insensitive)
    data = data[~data['sample_id'].str.contains("test", case=False, na=False)]
    
    # Convert non-standard NaN values to actual NaN
    data['reject_reason'] = data['reject_reason'].replace(['nan', 'NaN', 'None', '', ' '], pd.NA)

    # Remove rows where 'reject_reason' is not NaN
    data = data[data['reject_reason'].isna()]
    
    # Format scan_time to HR:MIN by removing the :SEC part if present
    data['scan_time'] = data['scan_time'].apply(lambda x: x[:5] if pd.notna(x) and len(x) > 5 else x)

    # If sample_id, scan_date and scan_time are all the same, throw error that contains the sample_id
    # and remove the rows except 1 of them.
    duplicates = data[data.duplicated(subset=['sample_id', 'scan_date', 'scan_time'], keep=False)]
    
    try:
        duplicates = data[data.duplicated(subset=['sample_id', 'scan_date', 'scan_time'], keep=False)]
        
        if not duplicates.empty:
            # Get the sample_ids of the duplicates
            duplicate_sample_ids = duplicates['sample_id'].unique()
            
            # Raise an error with the sample_ids
            raise ValueError(f"Duplicate rows found for sample_ids: {', '.join(map(str, duplicate_sample_ids))}")
    except ValueError as e:
        print(e)
        
    data = data.drop_duplicates(subset=['sample_id', 'scan_date', 'scan_time'], keep='first')
    
    # Rename special characters
    data.columns = data.columns.str.replace('%', '_percent').str.replace('#', '_number')

    # Remove superfluous columns
    columns_to_remove = ['patient_id', 'patient_name', 'patient_date_of_birth', 'sex', 'age']
    data = data.drop(columns=columns_to_remove, errors='ignore')

    # Add prover_complete
    data['prover_complete'] = '1'
    
    # Now rename variables to match REDcap
    new_colnames = [
    "sample_id", "sample_type", "slide_id", "kit_id", "wbc_109l", "wbc_flagged",
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
    
    if len(new_colnames) != len(data.columns):
        raise ValueError("The number of new column names must match the number of columns in the DataFrame")

    # Rename columns
    data.columns = new_colnames

    return data

def match_to_redcap(data_olo, project):
    """
    Matches OLO data to REDcap for a given project.
    
    Parameters:
    data_olo (DataFrame): The pandas DataFrame containing OLO data.
    project (str): The project identifier.
    
    Returns:
    DataFrame: The matched data.
    """
    # Using PyCap to export records and project info
    data_redcap = project.export_records(format_type='df')
    project_info = project.export_project_info()
    
    # Extract custom_record_label
    custom_record_label = project_info.get('custom_record_label', '')

    # Use regular expression to extract the part inside the brackets
    match = re.search(r'\[(.*?)\]', custom_record_label)
    if match:
        project_record_label = match.group(1)
    else:
        project_record_label = None

    # Find the index name of data_redcap
    index_name = data_redcap.index.name
    if index_name is None:
        index_name = 'index'
        data_redcap.reset_index(inplace=True)
        
    # Ensure the index column is included in the DataFrame columns
    if index_name not in data_redcap.columns:
        data_redcap[index_name] = data_redcap.index.astype(int)
    else:
        data_redcap[index_name] = data_redcap[index_name].astype(int)
    
    # Perform a left join on the REDCap data based on sample_id in data_olo and project_record_label in data_redcap
    data_ammended = pd.merge(
        data_olo, 
        data_redcap[[project_record_label, index_name]], 
        how='left', 
        left_on='sample_id', 
        right_on=project_record_label
    )
    
    # Convert index column to integer
    data_ammended[index_name] = data_ammended[index_name].astype('Int64')
    
    # Remove rows where the left join did not find a match
    data_ammended = data_ammended.dropna(subset=[index_name])
    
    # Remove the sample_id column
    data_ammended = data_ammended.drop(columns=['sample_id'])
    
    # Reorder columns to have index_name first, then project_record_label, then the rest
    cols = [index_name, project_record_label] + [col for col in data_ammended.columns if col not in [index_name, project_record_label]]
    data_ammended = data_ammended[cols]

    return data_ammended

def write_to_csv(df):
    """
    Writes the given DataFrame to a CSV file.
    
    Parameters:
    df (DataFrame): The pandas DataFrame to write to CSV.
    
    Returns:
    None
    """
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
    
def import_data(data_path, project):
    """
    Main function to import data for a given project.
    
    Parameters:
    data_path (str): The path to the data file.
    project (str): The project identifier.
    
    Returns:
    None
    """
    # Read and convert the data
    data_olo = read_convert(data_path)

    # Clean and fit the data
    data_cleaned = clean_olo(data_olo, project)

    # Match the data to REDCap
    data_matched = match_to_redcap(data_cleaned, project)
    
    # Import the data to REDcap
    project.import_records(data_matched, import_format='df')
    
    # Return the values from the second column
    second_column_name = data_matched.columns[1]
    return data_matched[second_column_name].tolist()