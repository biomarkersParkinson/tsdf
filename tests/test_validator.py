import unittest
from tsdf.constants import TestConstants as CONST
from tsdf import validator

class TestValidator(unittest.TestCase):

    def test_validate_valid_file(self):
        result = validator.validate_tsdf_format(CONST.TEST_DATA_FILES["ppp"])
        self.assertTrue(result)

    def test_validate_invalid_file(self):
        result = validator.validate_tsdf_format(CONST.TEST_DATA_FILES["missingkey"])
        self.assertFalse(result)
