import datetime
import unittest

from hatchet.api.schemas.validators import (
    modern_date_validator, modern_year_validator,
    score_validator
)


class ValidatorTestCase(unittest.TestCase):

    def test_year_validator_fails_old_years(self):
        self.assertFalse(modern_year_validator(1879))
        self.assertFalse(modern_year_validator(0))

    def test_year_validator_fails_negative_years(self):
        self.assertFalse(modern_year_validator(-1))
        self.assertFalse(modern_year_validator(-2019))

    def test_year_validator_fails_future_years(self):
        self.assertFalse(modern_year_validator(2025))
        self.assertFalse(modern_year_validator(9999))

    def test_year_validator_passes_modern_years(self):
        self.assertTrue(modern_year_validator(1900))
        self.assertTrue(modern_year_validator(2019))

    def test_date_validator_fails_old_date(self):
        old_date = datetime.date(1879, 1, 1)
        self.assertFalse(modern_date_validator(old_date))

    def test_date_validator_fails_future_date(self):
        future_date = datetime.date(2025, 1, 1)
        self.assertFalse(modern_date_validator(future_date))

    def test_score_validator(self):
        self.assertFalse(score_validator(-1))
        self.assertFalse(score_validator(101))
        self.assertTrue(score_validator(0))
        self.assertTrue(score_validator(1))
        self.assertTrue(score_validator(81))
