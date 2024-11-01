# test_alert_handling.py

import pytest
from src.utils.alert_handling import parse_condition

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
        (row['bp_right_sys'] != "" and (row['bp_right_sys'] < 80 or row['bp_right_sys'] > 180)) or
        (row['bp_left_sys'] != "" and (row['bp_left_sys'] < 80 or row['bp_left_sys'] > 180)) or
        (row['bp_right_dia'] != "" and (row['bp_right_dia'] < 50 or row['bp_right_dia'] > 110)) or
        (row['bp_left_dia'] != "" and (row['bp_left_dia'] < 50 or row['bp_left_dia'] > 110)) or
        (row['pulse_right'] != "" and (row['pulse_right'] < 40 or row['pulse_right'] > 120)) or
        (row['pulse_left'] != "" and (row['pulse_left'] < 40 or row['pulse_left'] > 120)) or
        (abs(row['bp_right_sys'] - row['bp_left_sys']) > 20) or
        (abs(row['bp_right_dia'] - row['bp_left_dia']) > 10)
    )
    '''
    parsed_condition = parse_condition(condition)
    assert parsed_condition.strip() == expected_output.strip()

def test_parse_condition_with_operators():
    condition = '([value] = 100) and ([status] >= 50)'
    expected_output = "(row['value'] == 100) and (row['status'] >= 50)"
    parsed_condition = parse_condition(condition)
    assert parsed_condition == expected_output

def test_parse_condition_with_functions():
    condition = '(abs([x]) > 10) or (round([y]) == 5)'
    expected_output = "(abs(row['x']) > 10) or (round(row['y']) == 5)"
    parsed_condition = parse_condition(condition)
    assert parsed_condition == expected_output

def test_parse_condition_no_variables():
    condition = '([constant] = 42)'
    expected_output = "(row['constant'] == 42)"
    parsed_condition = parse_condition(condition)
    assert parsed_condition == expected_output