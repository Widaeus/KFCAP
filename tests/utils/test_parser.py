import pytest
from src.utils.parser import parse, alerts_from_df_revised, check_deviations_revised
import pandas as pd
from unittest.mock import Mock
from src.models.alert import Alert

def test_parse_revised_lab():
    # Given condition string
    condition_str = '''
        ([wbc_109l] <> "" and ([wbc_109l] < 3.5 or [wbc_109l] > 12)) or
        ([plt_109l] <> "" and ([plt_109l] < 145 or [plt_109l] > 387)) or
        ([hgb_gl] <> "" and ([hgb_gl] < 117 or [hgb_gl] > 170)) or
        ([mcv_fl] <> "" and ([mcv_fl] < 80 or [mcv_fl] > 100)) or
        ([neut_number_109l] <> "" and ([neut_number_109l] < 1.6 or [neut_number_109l] > 8)) or
        ([lymph_number_109l] <> "" and ([lymph_number_109l] < 1.1 or [lymph_number_109l] > 3.5)) or
        ([mono_number_109l] <> "" and ([mono_number_109l] < 0.2 or [mono_number_109l] > 0.8)) or
        ([eos_number_109l] <> "" and ([eos_number_109l] < 0 or [eos_number_109l] > 0.5)) or
        ([baso_number_109l] <> "" and ([baso_number_109l] < 0 or [baso_number_109l] > 0.1))
    '''
    
    # Expected output with full structure
    expected_output = {
        "wbc_109l": {"conditions": "not empty AND (< 3.5 OR > 12)", "reference_interval": "3.5 < x < 12"},
        "plt_109l": {"conditions": "not empty AND (< 145 OR > 387)", "reference_interval": "145 < x < 387"},
        "hgb_gl": {"conditions": "not empty AND (< 117 OR > 170)", "reference_interval": "117 < x < 170"},
        "mcv_fl": {"conditions": "not empty AND (< 80 OR > 100)", "reference_interval": "80 < x < 100"},
        "neut_number_109l": {"conditions": "not empty AND (< 1.6 OR > 8)", "reference_interval": "1.6 < x < 8"},
        "lymph_number_109l": {"conditions": "not empty AND (< 1.1 OR > 3.5)", "reference_interval": "1.1 < x < 3.5"},
        "mono_number_109l": {"conditions": "not empty AND (< 0.2 OR > 0.8)", "reference_interval": "0.2 < x < 0.8"},
        "eos_number_109l": {"conditions": "not empty AND (< 0 OR > 0.5)", "reference_interval": "0 < x < 0.5"},
        "baso_number_109l": {"conditions": "not empty AND (< 0 OR > 0.1)", "reference_interval": "0 < x < 0.1"}
    }
    # Run the parse function
    result = parse(condition_str)
    
    # Assert that the result includes only the expected output structure
    for key in expected_output:
        assert result[key] == expected_output[key], f"Failed for key: {key}"

def test_parse_revised_bp():
    condition_str = '''
        (([bp_right_sys] <> "" and ([bp_right_sys] < 80 or [bp_right_sys] > 180)) or
        ([bp_left_sys] <> "" and ([bp_left_sys] < 80 or [bp_left_sys] > 180)) or
        ([bp_right_dia] <> "" and ([bp_right_dia] < 50 or [bp_right_dia] > 110)) or
        ([bp_left_dia] <> "" and ([bp_left_dia] < 50 or [bp_left_dia] > 110)) or
        ([pulse_right] <> "" and ([pulse_right] < 40 or [pulse_right] > 120)) or
        ([pulse_left] <> "" and ([pulse_left] < 40 or [pulse_left] > 120)) or
        (abs([bp_right_sys] - [bp_left_sys]) > 20) or
        (abs([bp_right_dia] - [bp_left_dia]) > 10)
        '''

    expected_output = {
        "bp_right_sys": {"conditions": 'not empty AND (< 80 OR > 180) OR (abs(bp_right_sys - bp_left_sys) > 20)', "reference_interval": '80 < x < 180'},
        "bp_left_sys": {"conditions": 'not empty AND (< 80 OR > 180) OR (abs(bp_right_sys - bp_left_sys) > 20)', "reference_interval": '80 < x < 180'},
        "bp_right_dia": {"conditions": 'not empty AND (< 50 OR > 110) OR (abs(bp_right_dia - bp_left_dia) > 10)', "reference_interval": '50 < x < 110'},
        "bp_left_dia": {"conditions": 'not empty AND (< 50 OR > 110) OR (abs(bp_right_dia - bp_left_dia) > 10)', "reference_interval": '50 < x < 110'},
        "pulse_right": {"conditions": 'not empty AND (< 40 OR > 120)', "reference_interval": '40 < x < 120'},
        "pulse_left": {"conditions": 'not empty AND (< 40 OR > 120)', "reference_interval": '40 < x < 120'}
    }
    
    # Run the parse function
    result = parse(condition_str)
    
    # Assert that the result includes only the expected output structure
    for key in expected_output:
        assert result[key] == expected_output[key], f"Failed for key: {key}"
        
def test_parse_revised_equals():
    condition_str = '''
        [cmr_notification] = 1 or [microvascdysfunction_cmr] = 1
        '''
        
    expected_otuput = {
        "cmr_notification": {"conditions": '= 1', "reference_interval": None},
        "microvascdysfunction_cmr": {"conditions": '= 1', "reference_interval": None}
    }
    
    # Run the parse function
    result = parse(condition_str)
    
    # Assert that the result includes only the expected output structure
    for key in expected_otuput:
        assert result[key] == expected_otuput[key], f"Failed for key: {key}"
        
def test_parse_revised_all():
    # Lab condition test case
    lab_condition_str = '''
        ([wbc_109l] <> "" and ([wbc_109l] < 3.5 or [wbc_109l] > 12)) or
        ([plt_109l] <> "" and ([plt_109l] < 145 or [plt_109l] > 387)) or
        ([hgb_gl] <> "" and ([hgb_gl] < 117 or [hgb_gl] > 170)) or
        ([mcv_fl] <> "" and ([mcv_fl] < 80 or [mcv_fl] > 100)) or
        ([neut_number_109l] <> "" and ([neut_number_109l] < 1.6 or [neut_number_109l] > 8)) or
        ([lymph_number_109l] <> "" and ([lymph_number_109l] < 1.1 or [lymph_number_109l] > 3.5)) or
        ([mono_number_109l] <> "" and ([mono_number_109l] < 0.2 or [mono_number_109l] > 0.8)) or
        ([eos_number_109l] <> "" and ([eos_number_109l] < 0 or [eos_number_109l] > 0.5)) or
        ([baso_number_109l] <> "" and ([baso_number_109l] < 0 or [baso_number_109l] > 0.1))
    '''
    expected_output_lab = {
        "wbc_109l": {"conditions": "not empty AND (< 3.5 OR > 12)", "reference_interval": "3.5 < x < 12"},
        "plt_109l": {"conditions": "not empty AND (< 145 OR > 387)", "reference_interval": "145 < x < 387"},
        "hgb_gl": {"conditions": "not empty AND (< 117 OR > 170)", "reference_interval": "117 < x < 170"},
        "mcv_fl": {"conditions": "not empty AND (< 80 OR > 100)", "reference_interval": "80 < x < 100"},
        "neut_number_109l": {"conditions": "not empty AND (< 1.6 OR > 8)", "reference_interval": "1.6 < x < 8"},
        "lymph_number_109l": {"conditions": "not empty AND (< 1.1 OR > 3.5)", "reference_interval": "1.1 < x < 3.5"},
        "mono_number_109l": {"conditions": "not empty AND (< 0.2 OR > 0.8)", "reference_interval": "0.2 < x < 0.8"},
        "eos_number_109l": {"conditions": "not empty AND (< 0 OR > 0.5)", "reference_interval": "0 < x < 0.5"},
        "baso_number_109l": {"conditions": "not empty AND (< 0 OR > 0.1)", "reference_interval": "0 < x < 0.1"}
    }
    result_lab = parse(lab_condition_str)
    for key in expected_output_lab:
        assert result_lab[key] == expected_output_lab[key], f"Failed for key: {key} in Lab conditions"

    # Blood pressure condition test case
    bp_condition_str = '''
        (([bp_right_sys] <> "" and ([bp_right_sys] < 80 or [bp_right_sys] > 180)) or
        ([bp_left_sys] <> "" and ([bp_left_sys] < 80 or [bp_left_sys] > 180)) or
        ([bp_right_dia] <> "" and ([bp_right_dia] < 50 or [bp_right_dia] > 110)) or
        ([bp_left_dia] <> "" and ([bp_left_dia] < 50 or [bp_left_dia] > 110)) or
        ([pulse_right] <> "" and ([pulse_right] < 40 or [pulse_right] > 120)) or
        ([pulse_left] <> "" and ([pulse_left] < 40 or [pulse_left] > 120)) or
        (abs([bp_right_sys] - [bp_left_sys]) > 20) or
        (abs([bp_right_dia] - [bp_left_dia]) > 10)
    '''
    expected_output_bp = {
        "bp_right_sys": {"conditions": 'not empty AND (< 80 OR > 180) OR (abs(bp_right_sys - bp_left_sys) > 20)', "reference_interval": '80 < x < 180'},
        "bp_left_sys": {"conditions": 'not empty AND (< 80 OR > 180) OR (abs(bp_right_sys - bp_left_sys) > 20)', "reference_interval": '80 < x < 180'},
        "bp_right_dia": {"conditions": 'not empty AND (< 50 OR > 110) OR (abs(bp_right_dia - bp_left_dia) > 10)', "reference_interval": '50 < x < 110'},
        "bp_left_dia": {"conditions": 'not empty AND (< 50 OR > 110) OR (abs(bp_right_dia - bp_left_dia) > 10)', "reference_interval": '50 < x < 110'},
        "pulse_right": {"conditions": 'not empty AND (< 40 OR > 120)', "reference_interval": '40 < x < 120'},
        "pulse_left": {"conditions": 'not empty AND (< 40 OR > 120)', "reference_interval": '40 < x < 120'}
    }
    result_bp = parse(bp_condition_str)
    for key in expected_output_bp:
        assert result_bp[key] == expected_output_bp[key], f"Failed for key: {key} in BP conditions"
        
    # Equality condition test case
    equals_condition_str = '''
        [cmr_notification] = 1 or [microvascdysfunction_cmr] = 1
    '''
    expected_output_equals = {
        "cmr_notification": {"conditions": '= 1', "reference_interval": None},
        "microvascdysfunction_cmr": {"conditions": '= 1', "reference_interval": None}
    }
    result_equals = parse(equals_condition_str)
    for key in expected_output_equals:
        assert result_equals[key] == expected_output_equals[key], f"Failed for key: {key} in Equals conditions"

def test_alerts_from_df_revised():
    data = {
        'alert-title': ['Alert 1', 'Alert 2'],
        'alert-condition': ['''([wbc_109l] <> "" and ([wbc_109l] < 3.5 or [wbc_109l] > 12)) or
        ([plt_109l] <> "" and ([plt_109l] < 145 or [plt_109l] > 387)) or
        ([hgb_gl] <> "" and ([hgb_gl] < 117 or [hgb_gl] > 170)) or
        ([mcv_fl] <> "" and ([mcv_fl] < 80 or [mcv_fl] > 100)) or
        ([neut_number_109l] <> "" and ([neut_number_109l] < 1.6 or [neut_number_109l] > 8)) or
        ([lymph_number_109l] <> "" and ([lymph_number_109l] < 1.1 or [lymph_number_109l] > 3.5)) or
        ([mono_number_109l] <> "" and ([mono_number_109l] < 0.2 or [mono_number_109l] > 0.8)) or
        ([eos_number_109l] <> "" and ([eos_number_109l] < 0 or [eos_number_109l] > 0.5)) or
        ([baso_number_109l] <> "" and ([baso_number_109l] < 0 or [baso_number_109l] > 0.1))''',
        '''(([bp_right_sys] <> "" and ([bp_right_sys] < 80 or [bp_right_sys] > 180)) or
        ([bp_left_sys] <> "" and ([bp_left_sys] < 80 or [bp_left_sys] > 180)) or
        ([bp_right_dia] <> "" and ([bp_right_dia] < 50 or [bp_right_dia] > 110)) or
        ([bp_left_dia] <> "" and ([bp_left_dia] < 50 or [bp_left_dia] > 110)) or
        ([pulse_right] <> "" and ([pulse_right] < 40 or [pulse_right] > 120)) or
        ([pulse_left] <> "" and ([pulse_left] < 40 or [pulse_left] > 120)) or
        (abs([bp_right_sys] - [bp_left_sys]) > 20) or
        (abs([bp_right_dia] - [bp_left_dia]) > 10))'''],
        'alert-deactivated': ['N', 'Y']
    }
    
    df = pd.DataFrame(data)

    # Create a mock project_instance
    project_instance = Mock()

    # Call the function
    alerts = alerts_from_df_revised(df, project_instance)

    # Verify the output
    assert len(alerts) == 2

    # Verify Alert 1
    assert alerts[0].title == 'Alert 1'
    assert alerts[0].alert_dict["wbc_109l"]["condition"] == 'not empty AND (< 3.5 OR > 12)'
    assert alerts[0].alert_dict["wbc_109l"]["reference_interval"] == '3.5 < x < 12'
    assert alerts[0].alert_dict["plt_109l"]["condition"] == 'not empty AND (< 145 OR > 387)'
    assert alerts[0].alert_dict["plt_109l"]["reference_interval"] == '145 < x < 387'
    assert alerts[0].active is True

    # Verify Alert 2
    assert alerts[1].title == 'Alert 2'
    assert alerts[1].alert_dict["bp_right_sys"]["condition"] == 'not empty AND (< 80 OR > 180) OR (abs(bp_right_sys - bp_left_sys) > 20)'
    assert alerts[1].alert_dict["bp_right_sys"]["reference_interval"] == '80 < x < 180'
    assert alerts[1].alert_dict["bp_left_sys"]["condition"] == 'not empty AND (< 80 OR > 180) OR (abs(bp_right_sys - bp_left_sys) > 20)'
    assert alerts[1].alert_dict["bp_left_sys"]["reference_interval"] == '80 < x < 180'
    assert alerts[1].alert_dict["bp_right_dia"]["condition"] == 'not empty AND (< 50 OR > 110) OR (abs(bp_right_dia - bp_left_dia) > 10)'
    assert alerts[1].alert_dict["bp_right_dia"]["reference_interval"] == '50 < x < 110'
    assert alerts[1].alert_dict["bp_left_dia"]["condition"] == 'not empty AND (< 50 OR > 110) OR (abs(bp_right_dia - bp_left_dia) > 10)'
    assert alerts[1].alert_dict["bp_left_dia"]["reference_interval"] == '50 < x < 110'
    assert alerts[1].alert_dict["pulse_right"]["condition"] == 'not empty AND (< 40 OR > 120)'
    assert alerts[1].alert_dict["pulse_right"]["reference_interval"] == '40 < x < 120'
    assert alerts[1].alert_dict["pulse_left"]["condition"] == 'not empty AND (< 40 OR > 120)'
    assert alerts[1].alert_dict["pulse_left"]["reference_interval"] == '40 < x < 120'
    assert alerts[1].active is False

    # Verify that the alerts were added to the project_instance
    assert project_instance.add_alert.call_count == 2
    project_instance.add_alert.assert_any_call('Alert 1', alerts[0].alert_dict, True)
    project_instance.add_alert.assert_any_call('Alert 2', alerts[1].alert_dict, False)

def test_check_deviations_revised():
    # Sample data with variables matching alert conditions
    df = pd.DataFrame({
        'record_id': ['MD1003', '3-1502'],
        'wbc_109l': [2.0, 4.0],  # 2.0 < 3.5, should trigger deviation for 'MD1003'
        'plt_109l': [100, 200],  # 100 < 145, should trigger deviation for 'MD1003'
        'hgb_gl': [110, 160],    # 110 < 117, should trigger deviation for 'MD1003'
        'mcv_fl': ["", 85],      # Empty value shouldnt be included
        'neut_number_109l': [1.0, 2.0],
        'lymph_number_109l': [0.5, 1.5],
        'mono_number_109l': [0.1, 0.3],
        'eos_number_109l': [0.0, 0.2],
        'baso_number_109l': [0.0, 0.05]
    })

    # Mock project instance with alert definitions
    project_instance = Mock()
    project_instance.export_project_info.return_value = {
        'custom_record_label': '[record_id]'
    }
    project_instance.alerts = [
        Alert("Alert 1", {
            "wbc_109l": {"condition": "not empty AND (< 3.5 OR > 12)", "reference_interval": "3.5 < x < 12"},
            "plt_109l": {"condition": "not empty AND (< 145 OR > 387)", "reference_interval": "145 < x < 387"}
        }, True),
        Alert("Alert 2", {
            "hgb_gl": {"condition": "not empty AND (< 117 OR > 170)", "reference_interval": "117 < x < 170"},
            "mcv_fl": {"condition": "not empty AND (< 80 OR > 100)", "reference_interval": "80 < x < 100"}
        }, True)
    ]

    # Mock find_study_id to return the identifier field
    global find_study_id
    find_study_id = Mock(return_value='record_id')

    # Run the check_deviations_revised function
    deviations = check_deviations_revised(df, project_instance)

    # Expected output based on the sample data and conditions
    expected_output = {
        'MD1003': [
            "wbc_109l",
            "plt_109l",
            "hgb_gl",
        ]
    }

    # Verify deviations match expected output
    for key in expected_output:
        assert key in deviations, f"Record {key} not found in deviations"
        assert set(deviations[key]) == set(expected_output[key]), f"Expected {expected_output[key]}, but got {deviations[key]}"

def test_check_deviations_revised():
    # Sample data with variables matching alert conditions, including BP and missing values
    df = pd.DataFrame({
        'record_id': ['MD1003', '3-1502'],
        'wbc_109l': [2.0, 4.0],            # 2.0 < 3.5, should trigger deviation for 'MD1003'
        'plt_109l': [100, 200],            # 100 < 145, should trigger deviation for 'MD1003'
        'hgb_gl': [110, 160],              # 110 < 117, should trigger deviation for 'MD1003'
        'mcv_fl': ["", 85],                # Empty value shouldn't be included
        'bp_right_sys': [75, 185],         # 75 < 80 for 'MD1003', 185 > 180 for '3-1502'
        'bp_left_sys': [82, 190],          # Normal for 'MD1003', 190 > 180 for '3-1502'
        'bp_right_dia': [45, ""],        # 45 < 50 for 'MD1003', missing value for '3-1502'
        'bp_left_dia': [55, 120],          # Normal for 'MD1003', 120 > 110 for '3-1502'
        'pulse_right': [38, 60],           # 38 < 40 for 'MD1003'
        'pulse_left': [42, 125],           # 125 > 120 for '3-1502'
        'neut_number_109l': [1.0, 2.0],
        'lymph_number_109l': [0.5, 1.5],
        'mono_number_109l': [0.1, 0.3],
        'eos_number_109l': [0.0, 0.2],
        'baso_number_109l': [0.0, 0.05]
    })

    # Mock project instance with alert definitions, including BP and pulse conditions
    project_instance = Mock()
    project_instance.export_project_info.return_value = {
        'custom_record_label': '[record_id]'
    }
    project_instance.alerts = [
        Alert("Alert 1", {
            "wbc_109l": {"condition": "not empty AND (< 3.5 OR > 12)", "reference_interval": "3.5 < x < 12"},
            "plt_109l": {"condition": "not empty AND (< 145 OR > 387)", "reference_interval": "145 < x < 387"}
        }, True),
        Alert("Alert 2", {
            "hgb_gl": {"condition": "not empty AND (< 117 OR > 170)", "reference_interval": "117 < x < 170"},
            "mcv_fl": {"condition": "not empty AND (< 80 OR > 100)", "reference_interval": "80 < x < 100"}
        }, True),
        Alert("Alert 3", {
            "bp_right_sys": {"condition": "not empty AND (< 80 OR > 180)", "reference_interval": "80 < x < 180"},
            "bp_left_sys": {"condition": "not empty AND (< 80 OR > 180)", "reference_interval": "80 < x < 180"},
            "bp_right_dia": {"condition": "not empty AND (< 50 OR > 110)", "reference_interval": "50 < x < 110"},
            "bp_left_dia": {"condition": "not empty AND (< 50 OR > 110)", "reference_interval": "50 < x < 110"},
            "pulse_right": {"condition": "not empty AND (< 40 OR > 120)", "reference_interval": "40 < x < 120"},
            "pulse_left": {"condition": "not empty AND (< 40 OR > 120)", "reference_interval": "40 < x < 120"}
        }, True)
    ]

    # Mock find_study_id to return the identifier field
    global find_study_id
    find_study_id = Mock(return_value='record_id')

    # Run the check_deviations_revised function
    deviations = check_deviations_revised(df, project_instance)

    # Expected output based on the sample data and conditions
    expected_output = {
        'MD1003': [
            "wbc_109l",
            "plt_109l",
            "hgb_gl",
            "bp_right_sys",
            "bp_right_dia",
            "pulse_right"
        ],
        '3-1502': [
            "bp_right_sys",
            "bp_left_sys",
            "bp_left_dia",
            "pulse_left"
        ]
    }

    # Verify deviations match expected output
    for key in expected_output:
        assert key in deviations, f"Record {key} not found in deviations"
        assert set(deviations[key]) == set(expected_output[key]), f"Expected {expected_output[key]}, but got {deviations[key]}"
