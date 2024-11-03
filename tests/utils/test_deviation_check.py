import pytest
from unittest.mock import Mock
import pandas as pd
from src.models.alert import Alert
from src.utils.alert_handling import create_alerts_from_dataframe, check_deviations, find_study_id
from src.utils.parsing import parse_conditions


def test_check_deviations():
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

    global find_study_id
    find_study_id = Mock(return_value='record_id')

    deviations = check_deviations(df, project_instance)

    expected_output = {
        'MD1003': [
            "wbc_109l",
            "plt_109l",
            "hgb_gl",
            "mcv_fl"
        ]
    }
    for key in expected_output:
        assert key in deviations
        assert set(deviations[key]) == set(expected_output[key]), f"Expected {expected_output[key]}, but got {deviations[key]}"


def test_check_deviations_with_missing_values():
    df = pd.DataFrame({
        'record_id': ['MD1003', '3-1502'],
        'wbc_109l': [2.0, 4.0],
        'plt_109l': [100, 500],
        'hgb_gl': [100, 160],
        'mcv_fl': [75, 85],
        'neut_number_109l': [1.0, 2.0],
        'lymph_number_109l': [0.5, 1.5],
        'mono_number_109l': [0.1, 0.3],
        'eos_number_109l': [0.0, 0.2],
        'baso_number_109l': [0.0, 0.05],
        'bp_right_sys': ['', 130],  # Missing blood pressure for MD1003
        'bp_left_sys': [120, 110]
    })

    project_instance = Mock()
    project_instance.export_project_info.return_value = {
        'custom_record_label': '[record_id]'
    }
    project_instance.alerts = [
        Alert("Alert 1", {
            "bp_right_sys": {"condition": "not empty, < 80, > 180", "reference_interval": "80.0 < x < 180.0"},
            "bp_left_sys": {"condition": "not empty, < 80, > 180", "reference_interval": "80.0 < x < 180.0"},
            "hgb_gl": {"condition": "not empty, < 117, > 170", "reference_interval": "117 < x < 170.0"},
            "plt_109l": {"condition": "not empty, < 145, > 387", "reference_interval": "145 < x < 387.0"}
        }, True)
    ]

    global find_study_id
    find_study_id = Mock(return_value='record_id')

    deviations = check_deviations(df, project_instance)

    expected_output = {
        'MD1003': [
            "hgb_gl",
            "plt_109l"
        ],
        '3-1502': [
            "plt_109l"
        ]
    }
    for key in expected_output:
        assert key in deviations
        assert set(deviations[key]) == set(expected_output[key]), f"Expected {expected_output[key]}, but got {deviations[key]}"


def test_check_deviations_with_abs_condition():
    df = pd.DataFrame({
        'record_id': ['MD1003', '3-1502'],
        'bp_right_sys': [130, 120],
        'bp_left_sys': [100, 120],
        'bp_right_dia': [90, 70],
        'bp_left_dia': [70, 70]
    })

    project_instance = Mock()
    project_instance.export_project_info.return_value = {
        'custom_record_label': '[record_id]'
    }
    project_instance.alerts = [
        Alert("Alert 1", {
            "bp_right_sys": {"condition": "abs(bp_right_sys - bp_left_sys) > 20", "reference_interval": "abs(bp_right_sys - bp_left_sys) > 20"},
            "bp_left_sys": {"condition": "abs(bp_right_sys - bp_left_sys) > 20", "reference_interval": "abs(bp_right_sys - bp_left_sys) > 20"},
            "bp_right_dia": {"condition": "abs(bp_right_dia - bp_left_dia) > 10", "reference_interval": "abs(bp_right_dia - bp_left_dia) > 10"},
            "bp_left_dia": {"condition": "abs(bp_right_dia - bp_left_dia) > 10", "reference_interval": "abs(bp_right_dia - bp_left_dia) > 10"}
        }, True)
    ]

    global find_study_id
    find_study_id = Mock(return_value='record_id')

    deviations = check_deviations(df, project_instance)

    expected_output = {
        'MD1003': [
            "bp_right_sys",
            "bp_left_sys",
            "bp_right_dia",
            "bp_left_dia"
        ]
    }
    for key in expected_output:
        assert key in deviations
        assert set(deviations[key]) == set(expected_output[key]), f"Expected {expected_output[key]}, but got {deviations[key]}"


def test_check_deviations_with_tricky_missing_values():
    df = pd.DataFrame({
        'record_id': ['MD1003', '3-1502'],
        'bp_right_sys': [130, None],  # Missing bp_right_sys for 3-1502
        'bp_left_sys': [100, 120],
        'bp_right_dia': [None, 95],  # Missing bp_right_dia for MD1003
        'bp_left_dia': [70, 75],
        'wbc_109l': [2.0, 4.0],  # Deviating for MD1003
        'plt_109l': [100, 500]   # Deviating for both
    })

    project_instance = Mock()
    project_instance.export_project_info.return_value = {
        'custom_record_label': '[record_id]'
    }
    project_instance.alerts = [
        Alert("Alert 1", {
            "bp_right_sys,bp_left_sys": {"condition": "abs(bp_right_sys - bp_left_sys) > 20", "reference_interval": "abs(bp_right_sys - bp_left_sys) > 20"},
            "bp_right_dia,bp_left_dia": {"condition": "abs(bp_right_dia - bp_left_dia) > 10", "reference_interval": "abs(bp_right_dia - bp_left_dia) > 10"},
            "wbc_109l": {"condition": "not empty, < 3.5, > 12", "reference_interval": "3.5 < x < 12.0"},
            "plt_109l": {"condition": "not empty, < 145, > 387", "reference_interval": "145 < x < 387.0"}
        }, True)
    ]

    global find_study_id
    find_study_id = Mock(return_value='record_id')

    deviations = check_deviations(df, project_instance)

    expected_output = {
        'MD1003': [
            "bp_right_sys",
            "bp_left_sys",
            "wbc_109l",
            "plt_109l"
        ],
        '3-1502': [
            "bp_right_dia",
            "bp_left_dia",
            "plt_109l"
        ]
    }
    for key in expected_output:
        assert key in deviations
        assert set(deviations[key]) == set(expected_output[key]), f"Expected {expected_output[key]}, but got {deviations[key]}"


def test_end_to_end_alerts_and_deviations_lab():
    # Step 1: Parse the condition string
    condition_str = '''
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

    expected_parsed_conditions = {
        "wbc_109l": {"conditions": "not empty, < 3.5, > 12", "reference_interval": "3.5 < x < 12.0"},
        "plt_109l": {"conditions": "not empty, < 145, > 387", "reference_interval": "145.0 < x < 387.0"},
        "hgb_gl": {"conditions": "not empty, < 117, > 170", "reference_interval": "117.0 < x < 170.0"},
        "mcv_fl": {"conditions": "not empty, < 80, > 100", "reference_interval": "80.0 < x < 100.0"},
        "neut_number_109l": {"conditions": "not empty, < 1.6, > 8", "reference_interval": "1.6 < x < 8.0"},
        "lymph_number_109l": {"conditions": "not empty, < 1.1, > 3.5", "reference_interval": "1.1 < x < 3.5"},
        "mono_number_109l": {"conditions": "not empty, < 0.2, > 0.8", "reference_interval": "0.2 < x < 0.8"},
        "eos_number_109l": {"conditions": "not empty, < 0.0, > 0.5", "reference_interval": "0.0 < x < 0.5"},
        "baso_number_109l": {"conditions": "not empty, < 0.0, > 0.1", "reference_interval": "0.0 < x < 0.1"}
    }

    parsed_conditions = parse_conditions(condition_str)
    assert parsed_conditions == expected_parsed_conditions, f"Expected {expected_parsed_conditions}, but got {parsed_conditions}"

    # Step 2: Create alerts from the DataFrame
    data = {
        'alert-title': ['Alert 1'],
        'alert-condition': [condition_str],
        'alert-deactivated': ['N']
    }
    
    df = pd.DataFrame(data)

    # Create a mock project_instance
    project_instance = Mock()
    project_instance.add_alert = Mock()
    project_instance.export_project_info.return_value = {
        'custom_record_label': '[record_id]'
    }

    # Call the function to create alerts
    alerts = create_alerts_from_dataframe(df, project_instance)
    project_instance.alerts = alerts
    
    # Verify the output
    assert len(alerts) == 1

    # Verify Alert 1
    assert alerts[0].title == 'Alert 1'
    for variable, details in expected_parsed_conditions.items():
        assert alerts[0].alert_dict[variable]["condition"] == details["conditions"]
        assert alerts[0].alert_dict[variable]["reference_interval"] == details["reference_interval"]
    assert alerts[0].active is True

    # Step 3: Check for deviating values in the DataFrame
    df_deviations = pd.DataFrame({
        'record_id': ['MD1003', '3-1502'],
        'wbc_109l': [2.0, 4.0],  # Deviating for MD1003
        'plt_109l': [100, 500],  # Deviating for both
        'hgb_gl': [110, 160], # Deviating for MD1003
        'mcv_fl': [75, 85], # Deviating for MD1003
        'neut_number_109l': [1.0, 2.0], # Deviating for MD1003
        'lymph_number_109l': [0.5, 1.5], # Deviating for MD1003
        'mono_number_109l': [0.1, 0.3], # Deviating for MD1003
        'eos_number_109l': [0.0, 0.2],
        'baso_number_109l': [0.0, 0.05]
    })

    # Mock the find_study_id function to return 'record_id'
    global find_study_id
    find_study_id = Mock(return_value='record_id')

    # Call the function to check deviations
    deviations = check_deviations(df_deviations, project_instance)

    # Verify the output
    expected_deviations = {
        'MD1003': [
            "wbc_109l",
            "plt_109l",
            "hgb_gl",
            "neut_number_109l",
            "lymph_number_109l",
            "mono_number_109l",
            "mcv_fl"
        ],
        '3-1502': [
            "plt_109l"
        ]
    }
    for key in expected_deviations:
        assert key in deviations
        assert set(deviations[key]) == set(expected_deviations[key]), f"Expected {expected_deviations[key]}, but got {deviations[key]}"


def test_end_to_end_alerts_and_deviations_bp():
    # Step 1: Parse the condition string
    condition_str = '''
        (([bp_right_sys] <> "" and ([bp_right_sys] < 80 or [bp_right_sys] > 180)) or
        ([bp_left_sys] <> "" and ([bp_left_sys] < 80 or [bp_left_sys] > 180)) or
        ([bp_right_dia] <> "" and ([bp_right_dia] < 50 or [bp_right_dia] > 110)) or
        ([bp_left_dia] <> "" and ([bp_left_dia] < 50 or [bp_left_dia] > 110)) or
        ([pulse_right] <> "" and ([pulse_right] < 40 or [pulse_right] > 120)) or
        ([pulse_left] <> "" and ([pulse_left] < 40 or [pulse_left] > 120)) or
        (abs([bp_right_sys] - [bp_left_sys]) > 20) or
        (abs([bp_right_dia] - [bp_left_dia]) > 10))
    '''

    expected_parsed_conditions = {
        "bp_right_sys": {"conditions": 'not empty, < 80, > 180', "reference_interval": '80.0 < x < 180.0'},
        "bp_left_sys": {"conditions": 'not empty, < 80, > 180', "reference_interval": '80.0 < x < 180.0'},
        "bp_right_dia": {"conditions": 'not empty, < 50, > 110', "reference_interval": '50.0 < x < 110.0'},
        "bp_left_dia": {"conditions": 'not empty, < 50, > 110', "reference_interval": '50.0 < x < 110.0'},
        "pulse_right": {"conditions": 'not empty, < 40, > 120', "reference_interval": '40.0 < x < 120.0'},
        "pulse_left": {"conditions": 'not empty, < 40, > 120', "reference_interval": '40.0 < x < 120.0'},
        "bp_right_sys,bp_left_sys": {"conditions": 'abs(bp_right_sys - bp_left_sys) > 20', "reference_interval": 'abs(bp_right_sys - bp_left_sys) > 20'},
        "bp_right_dia,bp_left_dia": {"conditions": 'abs(bp_right_dia - bp_left_dia) > 10', "reference_interval": 'abs(bp_right_dia - bp_left_dia) > 10'}
    }

    parsed_conditions = parse_conditions(condition_str)
    assert parsed_conditions == expected_parsed_conditions, f"Expected {expected_parsed_conditions}, but got {parsed_conditions}"

    # Step 2: Create alerts from the DataFrame
    data = {
        'alert-title': ['Alert 1'],
        'alert-condition': [condition_str],
        'alert-deactivated': ['N']
    }
    
    df = pd.DataFrame(data)

    # Create a mock project_instance
    project_instance = Mock()
    project_instance.add_alert = Mock()
    project_instance.export_project_info.return_value = {
        'custom_record_label': '[record_id]'
    }

    # Call the function to create alerts
    alerts = create_alerts_from_dataframe(df, project_instance)
    project_instance.alerts = alerts
    
    # Verify the output
    assert len(alerts) == 1

    # Step 3: Check for deviating values in the DataFrame
    df_deviations = pd.DataFrame({
        'record_id': ['MD1003', '3-1502'],
        'bp_right_sys': [130, 150], # Deviating for MD1003 and 3-1502
        'bp_left_sys': [100, 120], # Deviating for MD1003 and 3-1502
        'bp_right_dia': [90, 95], # Deviating for MD1003 and 3-1502
        'bp_left_dia': [70, 75], # Deviating for MD1003 and 3-1502
        'pulse_right': [50, 60],
        'pulse_left': [55, 65]
    })

    # Mock the find_study_id function to return 'record_id'
    global find_study_id
    find_study_id = Mock(return_value='record_id')

    # Call the function to check deviations
    deviations = check_deviations(df_deviations, project_instance)

    # Verify the output
    expected_deviations = {
        'MD1003': [
            "bp_right_sys",
            "bp_left_sys",
            "bp_right_dia",
            "bp_left_dia"
        ],
        '3-1502': [
            "bp_right_sys",
            "bp_left_sys",
            "bp_right_dia",
            "bp_left_dia"
        ]
    }
    for key in expected_deviations:
        assert key in deviations
        assert set(deviations[key]) == set(expected_deviations[key]), f"Expected {expected_deviations[key]}, but got {deviations[key]}"


if __name__ == "__main__":
    pytest.main()