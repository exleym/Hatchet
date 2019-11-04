import pytest
import hatchet.util as util


def test_record_stripper_works_for_single_digit_records():
    original = "Alabama (1-0)"
    expected = "Alabama"
    assert util.strip_record(original) == expected


def test_record_stripper_works_for_double_digit_wins():
    original = "Clemson (15-0)"
    expected = "Clemson"
    assert util.strip_record(original) == expected


def test_record_stripper_works_for_double_digit_losses():
    original = "South Carolina (0-11)"
    expected = "South Carolina"
    assert util.strip_record(original) == expected


def test_camel_to_snake_on_basic_dictionary():
    original = {
        "exampleA": 1,
        "exampleB": 2,
        "thisOneIsLong": 3
    }
    expected = {
        "example_a": 1,
        "example_b": 2,
        "this_one_is_long": 3
    }
    assert util.camel_to_snake(original) == expected
