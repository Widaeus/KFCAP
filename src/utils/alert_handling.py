import pandas as pd
from typing import List, Dict
import re
from src.models.alert import Alert
from src.models.session_manager import session_manager
from src.utils.parsing import parse_conditions


def create_alerts_from_dataframe(df: pd.DataFrame, project_instance) -> List[Alert]:
    """Create a list of Alert instances from a DataFrame of alert specifications."""
    all_alerts = []

    for _, row in df.iterrows():
        title = row['alert-title']
        condition_str = row['alert-condition']
        active = row['alert-deactivated'] == "N"

        parsed_conditions = parse_conditions(condition_str)
        
        # Create the alert dictionary
        alert_dict = {}
        for variable, details in parsed_conditions.items():
            alert_dict[variable] = {
                "condition": details["conditions"],
                "reference_interval": details.get("reference_interval")
            }

        # Add the alert to the project and collect in the list
        project_instance.add_alert(title, alert_dict, active)
        all_alerts.append(Alert(title, alert_dict, active))

    return all_alerts

def check_deviations(df: pd.DataFrame, project_instance) -> Dict[str, Dict]:
    """Identify variables and their deviation status based on dynamic conditions."""
    deviating_vars = {}
    study_id = find_study_id(project_instance)  # Obtain the record identifier field

    for _, row in df.iterrows():
        row_deviations = {}

        for alert in project_instance.alerts:
            for variable, details in alert.alert_dict.items():
                condition = details["condition"]
                reference_interval = details.get("reference_interval")

                # Parse the condition string
                conditions = condition.split(', ')
                eval_conditions = []
                for cond in conditions:
                    if 'not empty' in cond:
                        eval_conditions.append(f"row['{variable}'] == ''")
                    elif '<' in cond:
                        threshold = cond.split('<')[1].strip()
                        eval_conditions.append(f"row['{variable}'] < {threshold}")
                    elif '>' in cond:
                        threshold = cond.split('>')[1].strip()
                        eval_conditions.append(f"row['{variable}'] > {threshold}")

                # Combine the conditions with 'or'
                parsed_condition = ' or '.join(eval_conditions)

                try:
                    # Evaluate the parsed condition
                    if eval(parsed_condition, {"row": row.to_dict(), "pd": pd, "abs": abs}):
                        # Store deviation details only if the variable isn't already recorded
                        if variable not in row_deviations:
                            row_deviations[variable] = {
                                "condition": condition,
                                "reference_interval": reference_interval,
                                "value": float(row[variable]),  # Convert to standard Python float
                                "study_id": str(row[study_id])  # Ensure study_id is a string
                            }
                except Exception as e:
                    print(f"Error evaluating condition: {condition}\nError: {e}")

        if row_deviations:
            deviating_vars[str(row[study_id])] = row_deviations  # Use record_id as key

    return deviating_vars

def find_study_id(project):
    project_info = project.export_project_info()
    custom_record_label = project_info.get('custom_record_label', '')

    match = re.search(r'\[(.*?)\]', custom_record_label)
    if match:
        return match.group(1)
    return None

def load_csv(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    return df