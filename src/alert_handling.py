import pandas as pd
from typing import List
import re

def check_deviations(row: pd.Series) -> List[str]:
    deviating_vars = []

    # Blood Pressure and Pulse Alerts
    if pd.notna(row["bp_right_sys"]) and (row["bp_right_sys"] < 80 or row["bp_right_sys"] > 180):
        deviating_vars.append("bp_right_sys")
    if pd.notna(row["bp_left_sys"]) and (row["bp_left_sys"] < 80 or row["bp_left_sys"] > 180):
        deviating_vars.append("bp_left_sys")
    if pd.notna(row["bp_right_dia"]) and (row["bp_right_dia"] < 50 or row["bp_right_dia"] > 110):
        deviating_vars.append("bp_right_dia")
    if pd.notna(row["bp_left_dia"]) and (row["bp_left_dia"] < 50 or row["bp_left_dia"] > 110):
        deviating_vars.append("bp_left_dia")
    if pd.notna(row["pulse_right"]) and (row["pulse_right"] < 40 or row["pulse_right"] > 120):
        deviating_vars.append("pulse_right")
    if pd.notna(row["pulse_left"]) and (row["pulse_left"] < 40 or row["pulse_left"] > 120):
        deviating_vars.append("pulse_left")
    if pd.notna(row["bp_right_sys"]) and pd.notna(row["bp_left_sys"]) and abs(row["bp_right_sys"] - row["bp_left_sys"]) > 20:
        deviating_vars.append("bp_right_sys - bp_left_sys difference")
    if pd.notna(row["bp_right_dia"]) and pd.notna(row["bp_left_dia"]) and abs(row["bp_right_dia"] - row["bp_left_dia"]) > 10:
        deviating_vars.append("bp_right_dia - bp_left_dia difference")
    
    # Blood Counts and Hemoglobin Alerts
    if pd.notna(row["wbc_109l"]) and (row["wbc_109l"] < 3.5 or row["wbc_109l"] > 12):
        deviating_vars.append("wbc_109l")
    if pd.notna(row["plt_109l"]) and (row["plt_109l"] < 145 or row["plt_109l"] > 387):
        deviating_vars.append("plt_109l")
    if pd.notna(row["hgb_gl"]) and (row["hgb_gl"] < 117 or row["hgb_gl"] > 170):
        deviating_vars.append("hgb_gl")
    if pd.notna(row["mcv_fl"]) and (row["mcv_fl"] < 80 or row["mcv_fl"] > 100):
        deviating_vars.append("mcv_fl")
    if pd.notna(row["neut_number_109l"]) and (row["neut_number_109l"] < 1.6 or row["neut_number_109l"] > 8):
        deviating_vars.append("neut_number_109l")
    if pd.notna(row["lymph_number_109l"]) and (row["lymph_number_109l"] < 1.1 or row["lymph_number_109l"] > 3.5):
        deviating_vars.append("lymph_number_109l")
    if pd.notna(row["mono_number_109l"]) and (row["mono_number_109l"] < 0.2 or row["mono_number_109l"] > 0.8):
        deviating_vars.append("mono_number_109l")
    if pd.notna(row["eos_number_109l"]) and (row["eos_number_109l"] < 0.0 or row["eos_number_109l"] > 0.5):
        deviating_vars.append("eos_number_109l")
    if pd.notna(row["baso_number_109l"]) and (row["baso_number_109l"] < 0.0 or row["baso_number_109l"] > 0.1):
        deviating_vars.append("baso_number_109l")
    
    return deviating_vars

def find_study_id(project):
    project_info = project.export_project_info()
    custom_record_label = project_info.get('custom_record_label', '')

    # Use regular expression to extract the part inside the brackets
    match = re.search(r'\[(.*?)\]', custom_record_label)
    if match:
        project_record_label = match.group(1)
    else:
        project_record_label = None
    
    return project_record_label

def find_deviating_records(project) -> List[str]:
    deviating_ids = []
    deviations = {}
    study_id = find_study_id(project)
    data_redcap = project.export_records(format_type='df')

    for _, row in data_redcap.iterrows():
        deviating_vars = check_deviations(row)
        if deviating_vars:  # If there are deviations
            study_id_value = row[study_id]
            deviating_ids.append(study_id_value)
            deviations[study_id_value] = deviating_vars  # Store deviating variables

    return deviating_ids, deviations
