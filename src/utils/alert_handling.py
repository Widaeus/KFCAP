import pandas as pd
from typing import List, Dict
import re

def load_csv(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)

def parse_condition(condition: str) -> str:
    """Convert alert condition format to Python-evaluable expression."""
    condition = condition.replace("<>", "!=")
    condition = condition.replace("\n", "").strip()

    # Replace variable syntax from [var] to row['var']
    variables = re.findall(r'\[([^\]]+)\]', condition)
    for var in variables:
        condition = condition.replace(f"[{var}]", f"row['{var}']")
    
    return condition

def extract_variables(condition: str) -> List[str]:
    """Extract variable names from the condition."""
    variables = re.findall(r'\[([^\]]+)\]', condition)
    return list(set(variables))

def extract_reference_info(condition: str, variable: str) -> str:
    """Extract reference information for a variable from the condition."""
    # Split condition by 'or' and 'and'
    parts = re.split(r'\bor\b|\band\b', condition)
    references = []
    for part in parts:
        if f"[{variable}]" in part:
            ref = part.strip()
            references.append(ref)
    return ' and/or '.join(references)

def check_deviations(row: pd.Series, conditions: List[str]) -> Dict[str, Dict]:
    """Identify variables and their deviation status based on conditions."""
    variable_info = {}
    for condition in conditions:
        original_condition = condition  # Keep the original for reference info
        parsed_condition = parse_condition(condition)
        variables = extract_variables(condition)
        for var_name in variables:
            if var_name not in variable_info:
                variable_info[var_name] = {
                    'value': row[var_name] if var_name in row else None,
                    'deviated': False,
                    'reference': extract_reference_info(original_condition, var_name)
                }
        try:
            deviated = pd.notna(row[variables]).all() and eval(parsed_condition, {"row": row.to_dict(), "abs": abs})
            if deviated:
                for var_name in variables:
                    variable_info[var_name]['deviated'] = True
        except Exception as e:
            print(f"Error evaluating condition in row {row.to_dict()}: {e}")
    return variable_info  # Return info for all variables involved

def find_study_id(project):
    project_info = project.export_project_info()
    custom_record_label = project_info.get('custom_record_label', '')

    match = re.search(r'\[(.*?)\]', custom_record_label)
    if match:
        return match.group(1)
    return None

def find_deviating_records(project, alert_conditions: List[str]):
    """Find records and collect variable info including deviation status."""
    records_info = {}
    study_id = find_study_id(project)
    data_redcap = project.export_records(format_type='df')
    for _, row in data_redcap.iterrows():
        variable_info = check_deviations(row, alert_conditions)
        if variable_info:
            study_id_value = row[study_id]
            records_info[study_id_value] = variable_info
    return records_info  # Dict of {study_id: {var_name: {value, deviated, reference}}}

    alert_conditions = load_csv(alert_conditions_file)['conditions'].tolist()
    deviating_ids, deviations = find_deviating_records(project, alert_conditions)
    data_redcap = project.export_records(format_type='df')
    
    study_id_column = find_study_id(project)
    
    current_index = [0]

    alerts_window = ctk.CTkToplevel(root)
    alerts_window.title("Deviating Records")
    center_window(alerts_window, width=600, height=850)
    
    display_frame = ctk.CTkFrame(alerts_window)
    display_frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    # Display current study_id
    label_study_id = ctk.CTkLabel(display_frame, text="", font=("Arial", 14, "bold"))
    label_study_id.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

    # Column headers
    ctk.CTkLabel(display_frame, text="Variable", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=10, pady=5)
    ctk.CTkLabel(display_frame, text="Value", font=("Arial", 12, "bold")).grid(row=1, column=1, padx=10, pady=5)
    ctk.CTkLabel(display_frame, text="Reference", font=("Arial", 12, "bold")).grid(row=1, column=2, padx=10, pady=5)

    variable_names = [
        "bp_right_sys", "bp_left_sys", "bp_right_dia", "bp_left_dia", "pulse_right", "pulse_left",
        "wbc_109l", "plt_109l", "hgb_gl", "mcv_fl", "neut_number_109l", "lymph_number_109l",
        "mono_number_109l", "eos_number_109l", "baso_number_109l"
    ]

    plain_language_names = [
        "Systolic BP (Right)", "Systolic BP (Left)", "Diastolic BP (Right)", "Diastolic BP (Left)",
        "Pulse (Right)", "Pulse (Left)", "White Blood Cells", "Platelets", "Hemoglobin", "Mean Corpuscular Volume",
        "Neutrophils", "Lymphocytes", "Monocytes", "Eosinophils", "Basophils"
    ]
    
    reference_values = [
        "Reference: SysBP 80-180", "Reference: SysBP 80-180", "Reference: DiaBP 50-110", "Reference: DiaBP 50-110",
        "Reference: Pulse 40-120", "Reference: Pulse 40-120", "Reference: WBC 3.5-12", "Reference: Platelets 145-387",
        "Reference: Hemoglobin 117-170", "Reference: MCV 80-100", "Reference: Neutrophils 1.6-8", "Reference: Lymphocytes 1.1-3.5",
        "Reference: Monocytes 0.2-0.8", "Reference: Eosinophils 0.0-0.5", "Reference: Basophils 0.0-0.1"
    ]

    value_labels = []
    reference_labels = []

    for i, var_name in enumerate(variable_names):
        ctk.CTkLabel(display_frame, text=plain_language_names[i], font=("Arial", 12)).grid(row=i+2, column=0, padx=10, pady=5)
        value_label = ctk.CTkLabel(display_frame, text="", font=("Arial", 12))
        value_label.grid(row=i+2, column=1, padx=10, pady=5)
        value_labels.append(value_label)
        reference_label = ctk.CTkLabel(display_frame, text=reference_values[i], font=("Arial", 12))
        reference_label.grid(row=i+2, column=2, padx=10, pady=5)
        reference_labels.append(reference_label)

    def update_display():
        study_id = deviating_ids[current_index[0]]
        total_records = len(deviating_ids)
        label_study_id.configure(text=f"Study ID: {study_id} ({current_index[0] + 1}/{total_records} records)")
        row = data_redcap[data_redcap[study_id_column] == study_id].iloc[0]
        deviation_values = deviations[study_id]
        for i, var_name in enumerate(variable_names):
            value = row[var_name] if var_name in row else ""
            if var_name in deviation_values:
                value_labels[i].configure(text=str(value), font=("Arial", 12, "bold"), fg_color="red")
            else:
                value_labels[i].configure(text=str(value), font=("Arial", 12), fg_color="black")

        # Calculate and display differences
        systolic_diff = abs(row["bp_right_sys"] - row["bp_left_sys"]) if pd.notna(row["bp_right_sys"]) and pd.notna(row["bp_left_sys"]) else ""
        diastolic_diff = abs(row["bp_right_dia"] - row["bp_left_dia"]) if pd.notna(row["bp_right_dia"]) and pd.notna(row["bp_left_dia"]) else ""

        if "bp_right_sys - bp_left_sys difference" in deviation_values:
            systolic_diff_label.configure(text=str(systolic_diff), font=("Arial", 12, "bold"), fg_color="red")
        else:
            systolic_diff_label.configure(text=str(systolic_diff), font=("Arial", 12), fg_color="black")

        if "bp_right_dia - bp_left_dia difference" in deviation_values:
            diastolic_diff_label.configure(text=str(diastolic_diff), font=("Arial", 12, "bold"), fg_color="red")
        else:
            diastolic_diff_label.configure(text=str(diastolic_diff), font=("Arial", 12), fg_color="black")

    def next_record():
        if current_index[0] < len(deviating_ids) - 1:
            current_index[0] += 1
            update_display()

    def previous_record():
        if current_index[0] > 0:
            current_index[0] -= 1
            update_display()

    button_frame = ctk.CTkFrame(alerts_window)
    button_frame.pack(side="bottom", pady=10)

    button_previous = ctk.CTkButton(button_frame, text="Previous", command=previous_record, width=100, height=50)
    button_previous.pack(side="left", padx=10)

    button_next = ctk.CTkButton(button_frame, text="Next", command=next_record, width=100, height=50)
    button_next.pack(side="right", padx=10)

    update_display()