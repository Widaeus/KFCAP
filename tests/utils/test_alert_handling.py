import pytest
import pandas as pd
from src.utils.alert_handling import parse_condition, check_deviations, find_deviating_records
from typing import List, Dict
from unittest.mock import MagicMock

def test_parse_condition():
    condition = '''
    (
        ([bp_right_sys] <> "" and ([bp_right_sys] < 80 or [bp_right_sys] > 180)) or
        ([bp_left_sys] <> "" and ([bp_left_sys] < 80 or [bp_left_sys] > 180)) or
        ([bp_right_dia] <> "" and ([bp_right_dia] < 50 or [bp_right_dia] > 110)) or
        ([bp_left_dia] <> "" and ([bp_left_dia] < 50 or [bp_left_dia] > 110)) or
        ([pulse_right] <> "" and ([pulse_right] < 40 or [pulse_right] > 120)) or
        ([pulse_left] <> "" and ([pulse_left] < 40 or [pulse_left] > 120)) or
        (abs([bp_right_sys] - [bp_left_sys]) > 20) or
        (abs([bp_right_dia] - [bp_left_dia]) > 10)
    )
    '''
    expected_output = '''
    (
        (pd.notna(row["bp_right_sys"]) and (row["bp_right_sys"] < 80 or row["bp_right_sys"] > 180)) or
        (pd.notna(row["bp_left_sys"]) and (row["bp_left_sys"] < 80 or row["bp_left_sys"] > 180)) or
        (pd.notna(row["bp_right_dia"]) and (row["bp_right_dia"] < 50 or row["bp_right_dia"] > 110)) or
        (pd.notna(row["bp_left_dia"]) and (row["bp_left_dia"] < 50 or row["bp_left_dia"] > 110)) or
        (pd.notna(row["pulse_right"]) and (row["pulse_right"] < 40 or row["pulse_right"] > 120)) or
        (pd.notna(row["pulse_left"]) and (row["pulse_left"] < 40 or row["pulse_left"] > 120)) or
        (abs(row["bp_right_sys"] - row["bp_left_sys"]) > 20) or
        (abs(row["bp_right_dia"] - row["bp_left_dia"]) > 10)
    )
    '''
    parsed_condition = parse_condition(condition)
    assert parsed_condition.strip() == expected_output.strip()

def test_parse_condition_with_operators():
    condition = '([value] = 100) and ([status] >= 50)'
    expected_output = '(row["value"] == 100) and (row["status"] >= 50)'
    parsed_condition = parse_condition(condition)
    assert parsed_condition == expected_output

def test_parse_condition_with_functions():
    condition = '(abs([x]) > 10) or (round([y]) == 5)'
    expected_output = '(abs(row["x"]) > 10) or (round(row["y"]) == 5)'
    parsed_condition = parse_condition(condition)
    assert parsed_condition == expected_output

def test_parse_condition_no_variables():
    condition = '([constant] = 42)'
    expected_output = '(row["constant"] == 42)'
    parsed_condition = parse_condition(condition)
    assert parsed_condition == expected_output

def test_parse_condition_complex():
    condition = '''
        ([wbc_109l] <> "" and ([wbc_109l] < 3.5 or [wbc_109l] > 12)) or
        ([plt_109l] <> "" and ([plt_109l] < 145 or [plt_109l] > 387)) or
        ([hgb_gl] <> "" and ([hgb_gl] < 117 or [hgb_gl] > 170)) or
        ([mcv_fl] <> "" and ([mcv_fl] < 80 or [mcv_fl] > 100)) or
        ([neut_number_109l] <> "" and ([neut_number_109l] < 1.6 or [neut_number_109l] > 8)) or
        ([lymph_number_109l] <> "" and ([lymph_number_109l] < 1.1 or [lymph_number_109l] > 3.5)) or
        ([mono_number_109l] <> "" and ([mono_number_109l] < 0.2 or [mono_number_109l] > 0.8)) or
        ([eos_number_109l] <> "" and ([eos_number_109l] < 0.0 or [eos_number_109l] > 0.5)) or
        ([baso_number_109l] <> "" and ([baso_number_109l] < 0.0 or [baso_number_109l] > 0.1))
    '''
    
    expected_output = '''
        (pd.notna(row["wbc_109l"]) and (row["wbc_109l"] < 3.5 or row["wbc_109l"] > 12)) or
        (pd.notna(row["plt_109l"]) and (row["plt_109l"] < 145 or row["plt_109l"] > 387)) or
        (pd.notna(row["hgb_gl"]) and (row["hgb_gl"] < 117 or row["hgb_gl"] > 170)) or
        (pd.notna(row["mcv_fl"]) and (row["mcv_fl"] < 80 or row["mcv_fl"] > 100)) or
        (pd.notna(row["neut_number_109l"]) and (row["neut_number_109l"] < 1.6 or row["neut_number_109l"] > 8)) or
        (pd.notna(row["lymph_number_109l"]) and (row["lymph_number_109l"] < 1.1 or row["lymph_number_109l"] > 3.5)) or
        (pd.notna(row["mono_number_109l"]) and (row["mono_number_109l"] < 0.2 or row["mono_number_109l"] > 0.8)) or
        (pd.notna(row["eos_number_109l"]) and (row["eos_number_109l"] < 0.0 or row["eos_number_109l"] > 0.5)) or
        (pd.notna(row["baso_number_109l"]) and (row["baso_number_109l"] < 0.0 or row["baso_number_109l"] > 0.1))
    '''
    
    parsed_condition = parse_condition(condition)
    
    assert parsed_condition.replace(" ", "").replace("\n", "") == expected_output.replace(" ", "").replace("\n", "")

def test_check_deviations_single_condition():
    # Define a sample row and condition
    row = pd.Series({"bp_right_sys": 190, "bp_left_sys": 85, "pulse_right": 60})
    conditions = ["([bp_right_sys] <> \"\" and ([bp_right_sys] < 80 or [bp_right_sys] > 180))"]

    # Expected output
    expected_output = {
        "bp_right_sys": {
            "condition": "([bp_right_sys] <> \"\" and ([bp_right_sys] < 80 or [bp_right_sys] > 180))",
            "value": 190
        }
    }

    assert check_deviations(row, conditions) == expected_output

def test_check_deviations_multiple_conditions():
    # Define a sample row with multiple values deviating
    row = pd.Series({
        "bp_right_sys": 190, "bp_left_sys": 85, "pulse_right": 130, "wbc_109l": 13
    })
    conditions = [
        "([bp_right_sys] <> \"\" and ([bp_right_sys] < 80 or [bp_right_sys] > 180))",
        "([pulse_right] <> \"\" and ([pulse_right] < 40 or [pulse_right] > 120))",
        "([wbc_109l] <> \"\" and ([wbc_109l] < 3.5 or [wbc_109l] > 12))"
    ]

    # Expected output
    expected_output = {
        "bp_right_sys": {
            "condition": "([bp_right_sys] <> \"\" and ([bp_right_sys] < 80 or [bp_right_sys] > 180))",
            "value": 190
        },
        "pulse_right": {
            "condition": "([pulse_right] <> \"\" and ([pulse_right] < 40 or [pulse_right] > 120))",
            "value": 130
        },
        "wbc_109l": {
            "condition": "([wbc_109l] <> \"\" and ([wbc_109l] < 3.5 or [wbc_109l] > 12))",
            "value": 13
        }
    }

    assert check_deviations(row, conditions) == expected_output

def test_check_deviations_no_condition_met():
    # Define a sample row where no conditions are met
    row = pd.Series({"bp_right_sys": 120, "pulse_right": 70, "wbc_109l": 7})
    conditions = [
        "([bp_right_sys] <> \"\" and ([bp_right_sys] < 80 or [bp_right_sys] > 180))",
        "([pulse_right] <> \"\" and ([pulse_right] < 40 or [pulse_right] > 120))",
        "([wbc_109l] <> \"\" and ([wbc_109l] < 3.5 or [wbc_109l] > 12))"
    ]

    # Expected output: no deviations
    expected_output = {}

    assert check_deviations(row, conditions) == expected_output

def test_check_deviations_with_invalid_condition():
    # Define a sample row
    row = pd.Series({"bp_right_sys": 120, "pulse_right": 70})
    # Add an invalid condition
    conditions = ["([non_existing_var] <> \"\" and ([non_existing_var] < 50 or [non_existing_var] > 100))"]

    # Expected output: should handle gracefully with no deviations
    expected_output = {}

    assert check_deviations(row, conditions) == expected_output

alert_conditions = [
    "([bp_right_sys] <> \"\" and ([bp_right_sys] < 80 or [bp_right_sys] > 180))",
    "([pulse_right] <> \"\" and ([pulse_right] < 40 or [pulse_right] > 120))"
]

def test_find_deviating_records_single_deviation():
    # Mock data for a REDCap project with one record that should have a deviation
    mock_data = pd.DataFrame({
        "record_id": [1],
        "bp_right_sys": [190],
        "pulse_right": [60]
    })

    # Mock project with export_records and find_study_id methods
    mock_project = MagicMock()
    mock_project.export_records.return_value = mock_data
    # Set up export_project_info() to return a dictionary with custom_record_label
    mock_project.export_project_info.return_value = {"custom_record_label": "[record_id]"}

    # Test function
    result = find_deviating_records(mock_project, alert_conditions)
    expected_output = {
        1: {
            "bp_right_sys": {
                "condition": "([bp_right_sys] <> \"\" and ([bp_right_sys] < 80 or [bp_right_sys] > 180))",
                "value": 190
            }
        }
    }
    assert result == expected_output

def test_find_deviating_records_multiple_deviations_one_record():
    # Mock data with one record having multiple deviations
    mock_data = pd.DataFrame({
        "record_id": [1],
        "bp_right_sys": [190],
        "pulse_right": [130]
    })

    mock_project = MagicMock()
    mock_project.export_records.return_value = mock_data
    mock_project.export_project_info.return_value = {"custom_record_label": "[record_id]"}

    # Test function
    result = find_deviating_records(mock_project, alert_conditions)
    expected_output = {
        1: {
            "bp_right_sys": {
                "condition": "([bp_right_sys] <> \"\" and ([bp_right_sys] < 80 or [bp_right_sys] > 180))",
                "value": 190
            },
            "pulse_right": {
                "condition": "([pulse_right] <> \"\" and ([pulse_right] < 40 or [pulse_right] > 120))",
                "value": 130
            }
        }
    }
    assert result == expected_output

def test_find_deviating_records_no_deviation():
    # Mock data where all records are within normal ranges
    mock_data = pd.DataFrame({
        "record_id": [1],
        "bp_right_sys": [120],
        "pulse_right": [70]
    })

    mock_project = MagicMock()
    mock_project.export_records.return_value = mock_data
    mock_project.export_project_info.return_value = {"custom_record_label": "[record_id]"}

    # Test function
    result = find_deviating_records(mock_project, alert_conditions)
    expected_output = {}
    assert result == expected_output

def test_find_deviating_records_multiple_records():
    # Mock data with multiple records, some deviating and some not
    mock_data = pd.DataFrame({
        "record_id": [1, 2],
        "bp_right_sys": [190, 110],
        "pulse_right": [130, 60]
    })

    mock_project = MagicMock()
    mock_project.export_records.return_value = mock_data
    mock_project.export_project_info.return_value = {"custom_record_label": "[record_id]"}

    # Test function
    result = find_deviating_records(mock_project, alert_conditions)
    expected_output = {
        1: {
            "bp_right_sys": {
                "condition": "([bp_right_sys] <> \"\" and ([bp_right_sys] < 80 or [bp_right_sys] > 180))",
                "value": 190
            },
            "pulse_right": {
                "condition": "([pulse_right] <> \"\" and ([pulse_right] < 40 or [pulse_right] > 120))",
                "value": 130
            }
        }
    }
    assert result == expected_output

if __name__ == "__main__":
    pytest.main()