import datetime
import pytest
from hatchet.resources.schemas.validators import (
    modern_date_validator, modern_year_validator,
    score_validator
)
from hatchet.util.validators import validate_xor, validate_nand


def test_year_validator_fails_old_years():
    assert modern_year_validator(1879) is False
    assert modern_year_validator(0) is False


def test_year_validator_fails_negative_years():
    assert modern_year_validator(-1) is False
    assert modern_year_validator(-2019) is False


def test_year_validator_fails_future_years():
    assert modern_year_validator(2025) is False
    assert modern_year_validator(9999) is False


def test_year_validator_passes_modern_years():
    assert modern_year_validator(1900) is True
    assert modern_year_validator(2019) is True


def test_date_validator_fails_old_date():
    old_date = datetime.date(1879, 1, 1)
    assert modern_date_validator(old_date) is False


def test_date_validator_fails_future_date():
    future_date = datetime.date(2025, 1, 1)
    assert modern_date_validator(future_date) is False


def test_score_validator():
    assert score_validator(-1) is False
    assert score_validator(101) is False
    assert score_validator(0) is True
    assert score_validator(1) is True
    assert score_validator(81) is True


def test_validate_nand_passes_with_nulls():
    validate_nand(x=None)
    validate_nand(x=None, y=None)
    validate_nand(x=None, y=None, z=None)


def test_validate_nand_passes_with_single_int_param():
    validate_nand(x=1)
    validate_nand(x=None, y=1)
    validate_nand(x=None, y=None, z=1)
    validate_nand(x=None, y=1, z=None)


def test_validate_nand_passes_with_single_string_param():
    validate_nand(x="x")
    validate_nand(x=None, y="y")
    validate_nand(x=None, y=None, z="z")
    validate_nand(x="x", y=None, z=None)
    validate_nand(x=None, y="y", z=None)


def test_validate_nand_fails_with_two_ints():
    with pytest.raises(ValueError):
        validate_nand(x=1, y=1)


def test_validate_nand_fails_with_two_strings():
    with pytest.raises(ValueError):
        validate_nand(x="x", y="y")


def test_validate_nand_fails_with_two_falses():
    with pytest.raises(ValueError):
        validate_nand(x=False, y=False)


def test_validate_nand_passes_with_false():
    validate_nand(x=False)
    validate_nand(x=None, y=False)


def test_validate_xor_passes_with_single_int_param():
    validate_xor(x=1, y=None)
    validate_xor(x=None, y=2)


def test_validate_xor_fails_with_two_nulls():
    with pytest.raises(ValueError):
        validate_xor(x=None, y=None)


def test_validate_xor_fails_with_multiple_ints():
    with pytest.raises(ValueError):
        validate_xor(x=1, y=2, z=3)


def test_validate_xor_fails_with_multiple_strings():
    with pytest.raises(ValueError):
        validate_xor(x='x', y='y', z='z')
