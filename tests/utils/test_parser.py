import pytest
from src.utils.parsing import parse_conditions
import pandas as pd
from unittest.mock import Mock
from src.utils.alert_handling import create_alerts_from_dataframe

def test_parse_conditions():
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

    expected_output = {
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

    output = parse_conditions(condition_str)
    assert output == expected_output, f"Expected {expected_output}, but got {output}"
    
def test_create_alerts_from_dataframe():
    # Create a mock DataFrame
    data = {
        'alert-title': ['Alert 1', 'Alert 2'],
        'alert-condition': ['''([wbc_109l] <> "" and ([wbc_109l] < 3.5 or [wbc_109l] > 12)) or
        ([plt_109l] <> "" and ([plt_109l] < 145 or [plt_109l] > 387)) or
        ([hgb_gl] <> "" and ([hgb_gl] < 117 or [hgb_gl] > 170)) or
        ([mcv_fl] <> "" and ([mcv_fl] < 80 or [mcv_fl] > 100)) or
        ([neut_number_109l] <> "" and ([neut_number_109l] < 1.6 or [neut_number_109l] > 8)) or
        ([lymph_number_109l] <> "" and ([lymph_number_109l] < 1.1 or [lymph_number_109l] > 3.5)) or
        ([mono_number_109l] <> "" and ([mono_number_109l] < 0.2 or [mono_number_109l] > 0.8)) or
        ([eos_number_109l] <> "" and ([eos_number_109l] < 0.0 or [eos_number_109l] > 0.5)) or
        ([baso_number_109l] <> "" and ([baso_number_109l] < 0.0 or [baso_number_109l] > 0.1))''',
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
    alerts = create_alerts_from_dataframe(df, project_instance)

    # Verify the output
    assert len(alerts) == 2

    # Verify Alert 1
    assert alerts[0].title == 'Alert 1'
    assert alerts[0].alert_dict["wbc_109l"]["condition"] == 'not empty, < 3.5, > 12'
    assert alerts[0].alert_dict["plt_109l"]["condition"] == 'not empty, < 145, > 387'
    assert alerts[0].alert_dict["plt_109l"]["reference_interval"] == '145.0 < x < 387.0'
    assert alerts[0].active is True

    # Verify Alert 2
    assert alerts[1].title == 'Alert 2'
    assert alerts[1].alert_dict["bp_right_sys"]["condition"] == 'not empty, < 80, > 180'
    assert alerts[1].alert_dict["bp_right_sys"]["reference_interval"] == '80.0 < x < 180.0'
    assert alerts[1].alert_dict["bp_left_sys"]["condition"] == 'not empty, < 80, > 180'
    assert alerts[1].alert_dict["bp_left_sys"]["reference_interval"] == '80.0 < x < 180.0'
    assert alerts[1].alert_dict["bp_right_dia"]["condition"] == 'not empty, < 50, > 110'
    assert alerts[1].alert_dict["bp_right_dia"]["reference_interval"] == '50.0 < x < 110.0'
    assert alerts[1].alert_dict["bp_left_dia"]["condition"] == 'not empty, < 50, > 110'
    assert alerts[1].alert_dict["bp_left_dia"]["reference_interval"] == '50.0 < x < 110.0'
    assert alerts[1].alert_dict["pulse_right"]["condition"] == 'not empty, < 40, > 120'
    assert alerts[1].alert_dict["pulse_right"]["reference_interval"] == '40.0 < x < 120.0'
    assert alerts[1].alert_dict["pulse_left"]["condition"] == 'not empty, < 40, > 120'
    assert alerts[1].alert_dict["pulse_left"]["reference_interval"] == '40.0 < x < 120.0'
    assert alerts[1].alert_dict["bp_right_sys,bp_left_sys"]["condition"] == 'abs(bp_right_sys - bp_left_sys) > 20'
    assert alerts[1].alert_dict["bp_right_sys,bp_left_sys"]["reference_interval"] == 'abs(bp_right_sys - bp_left_sys) > 20'
    assert alerts[1].alert_dict["bp_right_dia,bp_left_dia"]["condition"] == 'abs(bp_right_dia - bp_left_dia) > 10'
    assert alerts[1].alert_dict["bp_right_dia,bp_left_dia"]["reference_interval"] == 'abs(bp_right_dia - bp_left_dia) > 10'
    assert alerts[1].active is False

    # Verify that the alerts were added to the project_instance
    assert project_instance.add_alert.call_count == 2
    project_instance.add_alert.assert_any_call('Alert 1', alerts[0].alert_dict, True)
    project_instance.add_alert.assert_any_call('Alert 2', alerts[1].alert_dict, False)


if __name__ == "__main__":
    pytest.main()