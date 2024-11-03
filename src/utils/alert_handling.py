import pandas as pd
from typing import List, Dict
import re
from src.models.alert import Alert
from src.models.session_manager import session_manager
from src.utils.parsing import parse_conditions


def create_alerts_from_dataframe(df: pd.DataFrame, project_instance) -> List[Alert]:
    all_alerts = []

    for _, row in df.iterrows():
        title = row['alert-title']
        condition_str = row['alert-condition']
        active = row['alert-deactivated'] == "N"

        parsed_conditions = parse_conditions(condition_str)
        
        alert_dict = {}
        for variable, details in parsed_conditions.items():
            if "," in variable:
                var1, var2 = [v.strip() for v in variable.split(",")]

                # Append conditions if variable already exists
                if var1 in alert_dict:
                    alert_dict[var1]["condition"] += f", {details['conditions']}"
                else:
                    alert_dict[var1] = {
                        "condition": details["conditions"],
                        "reference_interval": details.get("reference_interval"),
                        "paired_with": var2
                    }

                if var2 in alert_dict:
                    alert_dict[var2]["condition"] += f", {details['conditions']}"
                else:
                    alert_dict[var2] = {
                        "condition": details["conditions"],
                        "reference_interval": details.get("reference_interval"),
                        "paired_with": var1
                    }
            else:
                # Append conditions if variable already exists
                if variable in alert_dict:
                    alert_dict[variable]["condition"] += f", {details['conditions']}"
                else:
                    alert_dict[variable] = {
                        "condition": details["conditions"],
                        "reference_interval": details.get("reference_interval")
                    }

        project_instance.add_alert(title, alert_dict, active)
        all_alerts.append(Alert(title, alert_dict, active))

    return all_alerts


def check_deviations(df: pd.DataFrame, project_instance) -> Dict[str, List[str]]:
    """Identify variables with deviation based on dynamic conditions and return variable names with study_id."""
    deviating_vars = {}
    study_id = find_study_id(project_instance)  # Obtain the record identifier field

    for _, row in df.iterrows():
        row_deviations = set()  # Use a set to prevent duplicate entries

        for alert in project_instance.alerts:
            for variable, details in alert.alert_dict.items():
                condition = details["condition"]
                conditions = condition.split(', ')
                is_deviating = False

                for cond in conditions:
                    # Handle absolute difference condition for paired variables
                    if cond.startswith('abs('):
                        var_pair = cond[4:].split(')')[0]
                        var1, var2 = [v.strip() for v in var_pair.split('-')]
                        
                        # Ensure valid data is present for both variables
                        if pd.isna(row[var1]) or row[var1] == "" or pd.isna(row[var2]) or row[var2] == "":
                            is_deviating = False
                            break

                        # Check if absolute difference exceeds threshold
                        threshold = float(cond.split('>')[1].strip())
                        if abs(row[var1] - row[var2]) > threshold:
                            is_deviating = True
                            row_deviations.update([var1, var2])  # Add both variables to the set
                            break  # Only append once per condition

                    # Handle non-absolute difference conditions (e.g., '<', '>', 'not empty')
                    elif 'not empty' in cond:
                        if row[variable] == "":
                            is_deviating = False
                            break
                    elif '<' in cond:
                        threshold = float(cond.split('<')[1].strip())
                        if row[variable] < threshold:
                            is_deviating = True
                    elif '>' in cond:
                        threshold = float(cond.split('>')[1].strip())
                        if row[variable] > threshold:
                            is_deviating = True

                # Append single-variable deviations if condition met
                if is_deviating and not cond.startswith('abs('):
                    row_deviations.add(variable)

        if row_deviations:
            deviating_vars[str(row[study_id])] = list(row_deviations)  # Convert set to list

    return deviating_vars


def find_study_id(project):
    project_info = project.export_project_info()
    custom_record_label = project_info.get('custom_record_label', '')

    match = re.search(r'\[(.*?)\]', custom_record_label)
    if match:
        study_id = match.group(1)
        # Sanitize study_id by removing illegal characters
        study_id = re.sub(r'[^\w\-]', '', study_id)
        return study_id
    return None


def load_csv(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    return df