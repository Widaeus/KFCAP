import re
import pandas as pd
from typing import List, Dict
from src.models.alert import Alert
from src.utils.utils import find_study_id

def parse(condition_str):
    """
    Parses the condition string and converts it to a dictionary structure with conditions and reference intervals.
    This extended version accounts for conditions involving absolute differences.
    """
 # Patterns to match various types of conditions
    basic_pattern = r'\(\[(?P<var>\w+)\] <> "" and \(\[(?P<var2>\w+)\] (?P<ltgt1><|>) (?P<val1>[\d.]+) or \[(?P<var3>\w+)\] (?P<ltgt2><|>) (?P<val2>[\d.]+)\)\)'
    abs_pattern = r'\(abs\(\[(?P<var1>\w+)\] - \[(?P<var2>\w+)\]\) > (?P<threshold>[\d.]+)\)'
    equality_pattern = r'\[(?P<var>\w+)\] = (?P<value>[\d.]+)'

    result = {}

    # Parse basic range conditions
    matches = re.finditer(basic_pattern, condition_str)
    for match in matches:
        var = match.group("var")
        ltgt1, val1 = match.group("ltgt1"), match.group("val1")
        ltgt2, val2 = match.group("ltgt2"), match.group("val2")

        # Build the reference interval in the format `min < x < max`
        if ltgt1 == '<':
            reference_interval = f"{val1} < x < {val2}"
        else:
            reference_interval = f"{val2} < x < {val1}"

        # Build the conditions for the variable
        conditions = "not empty AND ({} {} OR {} {})".format(ltgt1, val1, ltgt2, val2)

        # Add to result dictionary
        result[var] = {
            "conditions": conditions,
            "reference_interval": reference_interval
        }

    # Parse absolute difference conditions
    abs_matches = re.finditer(abs_pattern, condition_str)
    for abs_match in abs_matches:
        var1 = abs_match.group("var1")
        var2 = abs_match.group("var2")
        threshold = abs_match.group("threshold")

        # Construct the absolute condition string
        abs_condition_str = f"abs({var1} - {var2}) > {threshold}"
        
        # Extend the conditions for variables involved in abs()
        for var in [var1, var2]:
            if var in result:
                result[var]["conditions"] += f" OR ({abs_condition_str})"
            else:
                # Set up entry if the variable is isolated to abs() condition
                result[var] = {
                    "conditions": f"({abs_condition_str})",
                    "reference_interval": ""
                }
    
    # Parse equality-based conditions
    equality_matches = re.finditer(equality_pattern, condition_str)
    for equality_match in equality_matches:
        var = equality_match.group("var")
        value = equality_match.group("value")
        
        # Set up entry for equality conditions
        result[var] = {
            "conditions": f"= {value}",
            "reference_interval": None
        }
    
    return result

def alerts_from_df_revised(df: pd.DataFrame, project_instance) -> List[Alert]:
    all_alerts = []

    for _, row in df.iterrows():
        title = row['alert-title']
        condition_str = row['alert-condition']
        active = row['alert-deactivated'] == "N"

        parsed_conditions = parse(condition_str)
        
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

def check_deviations_revised(df: pd.DataFrame, project_instance) -> Dict[str, List[str]]:
    """Identify variables with deviations based on dynamic conditions and return variable names with study_id."""
    deviating_vars = {}
    study_id = find_study_id(project_instance)  # Obtain the record identifier field

    for _, row in df.iterrows():
        row_deviations = set()  # Use a set to prevent duplicate entries

        for alert in project_instance.alerts:
            for variable, details in alert.alert_dict.items():
                condition = details["condition"]

                # Split conditions by "OR" and evaluate each group separately
                or_conditions = condition.split(' OR ')
                is_deviating = False

                for or_cond in or_conditions:
                    # Further split each OR condition by "AND" and evaluate all parts
                    and_conditions = or_cond.split(' AND ')
                    and_deviation = True  # Each part in AND conditions must be True

                    for cond in and_conditions:
                        cond = cond.strip()

                        # Absolute difference condition
                        if cond.startswith('abs('):
                            var_pair = cond[4:].split(')')[0]
                            var1, var2 = [v.strip() for v in var_pair.split('-')]

                            # Ensure valid data is present for both variables
                            try:
                                val1 = float(row[var1])
                                val2 = float(row[var2])
                            except (ValueError, TypeError):
                                and_deviation = False
                                break

                            # Check if absolute difference exceeds threshold
                            threshold = float(cond.split('>')[1].replace(')', '').strip())
                            if abs(val1 - val2) <= threshold:
                                and_deviation = False
                                break

                        # "not empty" condition
                        elif 'not empty' in cond:
                            if pd.isna(row[variable]) or row[variable] == "":
                                and_deviation = False
                                break

                        # "<" condition
                        elif '<' in cond:
                            try:
                                threshold = float(cond.split('<')[1].replace(')', '').strip())
                                if float(row[variable]) >= threshold:
                                    and_deviation = False
                                    break
                            except (ValueError, TypeError):
                                and_deviation = False
                                break

                        # ">" condition
                        elif '>' in cond:
                            try:
                                threshold = float(cond.split('>')[1].replace(')', '').strip())
                                if float(row[variable]) <= threshold:
                                    and_deviation = False
                                    break
                            except (ValueError, TypeError):
                                and_deviation = False
                                break

                    # If all AND conditions in this OR group are met, mark as deviating
                    if and_deviation:
                        is_deviating = True
                        row_deviations.add(variable)
                        break  # Stop evaluating further OR conditions if one is met

                if is_deviating:
                    row_deviations.add(variable)

        # Add the row's deviations to the final dictionary if any deviations found
        if row_deviations:
            deviating_vars[str(row[study_id])] = list(row_deviations)  # Convert set to list

    return deviating_vars