import pandas as pd
from typing import List, Dict
import re

def load_csv(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)

def parse_condition(condition: str) -> str:
    """Convert alert condition format to Python-evaluable expression."""
    condition = re.sub(r'\[([^\]]+)\]', r'row["\1"]', condition)
    condition = re.sub(r'(?<![><!])(?<![=])=(?!=)', '==', condition)
    condition = condition.replace("<>", "!=")
    condition = re.sub(r'row\["([^"]+)"\]\s*!=\s*""', r'pd.notna(row["\1"])', condition)
    condition = re.sub(r'row\["([^"]+)"\]\s*==\s*""', r'pd.isna(row["\1"])', condition)
    condition = condition.strip()
    return condition

def check_deviations(row: pd.Series, conditions: List[str]) -> Dict[str, Dict]:
    """Identify variables and their deviation status based on dynamic conditions."""
    deviating_vars = {}

    for condition in conditions:
        # Parse each condition to convert to Python-evaluable syntax
        parsed_condition = parse_condition(condition)
        try:
            # Evaluate the parsed condition
            if eval(parsed_condition, {"row": row.to_dict(), "pd": pd, "abs": abs}):
                # Extract variable names from the condition to specify which variable deviates
                variables = re.findall(r'row\["([^"]+)"\]', parsed_condition)
                for var in variables:
                    # Store deviation details only if the variable isn't already recorded
                    if var not in deviating_vars:
                        deviating_vars[var] = {
                            "condition": condition,
                            "value": row[var]
                        }
        except Exception as e:
            print(f"Error evaluating condition: {condition}\nError: {e}")
    
    return deviating_vars

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
    study_id = find_study_id(project)  # Obtain the record identifier field
    data_redcap = project.export_records(format_type='df')  # Export data as DataFrame

    for _, row in data_redcap.iterrows():
        # Check deviations for the current row
        variable_info = check_deviations(row, alert_conditions)
        if variable_info:  # Only include records with deviations
            study_id_value = row[study_id]  # Extract the record ID for this row
            records_info[study_id_value] = variable_info  # Associate deviations with the record ID
    
    return records_info