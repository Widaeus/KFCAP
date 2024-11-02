import pytest
from unittest.mock import Mock
from src.models.alert import Alert
from src.utils.alert_handling import check_deviations
import pandas as pd

def test_check_deviations():
    # Create a mock DataFrame with test values including study_id
    df = pd.DataFrame({
        'record_id': ['MD1003', '3-1502'],
        'wbc_109l': [2.0, 4.0],
        'plt_109l': [100, 200],
        'hgb_gl': [110, 160],
        'mcv_fl': [75, 85],
        'neut_number_109l': [1.0, 2.0],
        'lymph_number_109l': [0.5, 1.5],
        'mono_number_109l': [0.1, 0.3],
        'eos_number_109l': [0.0, 0.2],
        'baso_number_109l': [0.0, 0.05]
    })

    # Create a mock project_instance with export_project_info method
    project_instance = Mock()
    project_instance.export_project_info.return_value = {
        'custom_record_label': '[record_id]'
    }
    project_instance.alerts = [
        Alert("Alert 1", {
            "wbc_109l": {"condition": "not empty, < 3.5, > 12", "reference_interval": "3.5 < x < 12.0"},
            "plt_109l": {"condition": "not empty, < 145, > 387", "reference_interval": "145 < x < 387.0"}
        }, True),
        Alert("Alert 2", {
            "hgb_gl": {"condition": "not empty, < 117, > 170", "reference_interval": "117 < x < 170.0"},
            "mcv_fl": {"condition": "not empty, < 80, > 100", "reference_interval": "80 < x < 100.0"}
        }, True)
    ]

    # Mock the find_study_id function to return 'record_id'
    global find_study_id
    find_study_id = Mock(return_value='record_id')

    # Call the function
    deviations = check_deviations(df, project_instance)

    # Verify the output
    expected_output = {
        'MD1003': {
            "wbc_109l": {"condition": "not empty, < 3.5, > 12", "reference_interval": "3.5 < x < 12.0", "value": 2.0, "study_id": 'MD1003'},
            "plt_109l": {"condition": "not empty, < 145, > 387", "reference_interval": "145 < x < 387.0", "value": 100, "study_id": 'MD1003'},
            "hgb_gl": {"condition": "not empty, < 117, > 170", "reference_interval": "117 < x < 170.0", "value": 110, "study_id": 'MD1003'},
            "mcv_fl": {"condition": "not empty, < 80, > 100", "reference_interval": "80 < x < 100.0", "value": 75, "study_id": 'MD1003'}
        }
    }
    assert deviations == expected_output, f"Expected {expected_output}, but got {deviations}"

def test_check_deviations_with_missing_values():
    # Create a mock DataFrame with test values including study_id and missing blood pressure
    df = pd.DataFrame({
        'record_id': ['MD1003', '3-1502'],
        'wbc_109l': [2.0, 4.0],
        'plt_109l': [100, 200],
        'hgb_gl': [110, 160],
        'mcv_fl': [75, 85],
        'neut_number_109l': [1.0, 2.0],
        'lymph_number_109l': [0.5, 1.5],
        'mono_number_109l': [0.1, 0.3],
        'eos_number_109l': [0.0, 0.2],
        'baso_number_109l': [0.0, 0.05],
        'bp_right_sys': ['', 130],  # Missing blood pressure for MD1003
        'bp_left_sys': [120, 110]
    })

    # Create a mock project_instance with export_project_info method
    project_instance = Mock()
    project_instance.export_project_info.return_value = {
        'custom_record_label': '[record_id]'
    }
    project_instance.alerts = [
        Alert("Alert 1", {
            "bp_right_sys": {"condition": "not empty, < 80, > 180", "reference_interval": "80.0 < x < 180.0"},
            "bp_left_sys": {"condition": "not empty, < 80, > 180", "reference_interval": "80.0 < x < 180.0"}
        }, True)
    ]

    # Mock the find_study_id function to return 'record_id'
    global find_study_id
    find_study_id = Mock(return_value='record_id')

    # Call the function
    deviations = check_deviations(df, project_instance)

    # Verify the output
    expected_output = {
        '3-MD1003': {
            "bp_right_sys": {"condition": "not empty, < 80, > 180", "reference_interval": "80.0 < x < 180.0", "value": '', "study_id": '3-1502'}
        }
    }
    assert deviations == expected_output, f"Expected {expected_output}, but got {deviations}"

def test_check_deviations_with_abs_condition():
    # Create a mock DataFrame with test values including study_id and absolute difference condition
    df = pd.DataFrame({
        'record_id': ['MD1003', '3-1502'],
        'bp_right_sys': [130, 150],
        'bp_left_sys': [100, 120],
        'bp_right_dia': [90, 95],
        'bp_left_dia': [70, 75]
    })

    # Create a mock project_instance with export_project_info method
    project_instance = Mock()
    project_instance.export_project_info.return_value = {
        'custom_record_label': '[record_id]'
    }
    project_instance.alerts = [
        Alert("Alert 1", {
            "bp_right_sys,bp_left_sys": {"condition": "abs(bp_right_sys - bp_left_sys) > 20", "reference_interval": "abs(bp_right_sys - bp_left_sys) > 20"},
            "bp_right_dia,bp_left_dia": {"condition": "abs(bp_right_dia - bp_left_dia) > 10", "reference_interval": "abs(bp_right_dia - bp_left_dia) > 10"}
        }, True)
    ]

    # Mock the find_study_id function to return 'record_id'
    global find_study_id
    find_study_id = Mock(return_value='record_id')

    # Call the function
    deviations = check_deviations(df, project_instance)

    # Verify the output
    expected_output = {
        'MD1003': {
            "bp_right_sys,bp_left_sys": {"condition": "abs(bp_right_sys - bp_left_sys) > 20", "reference_interval": "abs(bp_right_sys - bp_left_sys) > 20", "value": 30, "study_id": 'MD1003'},
            "bp_right_dia,bp_left_dia": {"condition": "abs(bp_right_dia - bp_left_dia) > 10", "reference_interval": "abs(bp_right_dia - bp_left_dia) > 10", "value": 20, "study_id": 'MD1003'}
        }
    }
    assert deviations == expected_output, f"Expected {expected_output}, but got {deviations}"

if __name__ == "__main__":
    pytest.main()