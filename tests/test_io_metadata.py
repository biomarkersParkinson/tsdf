import json
import os
import unittest
from tsdf import io_metadata

from tsdf.tsdf_metadata import TSDFMetadata

_TESTDATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
TESTDATA = { "flat"         : os.path.join(_TESTDATA_DIR, 'data/flat.json'),
             "hierarchical" : os.path.join(_TESTDATA_DIR, 'hierarchical.json'),
             "wrongversion" : os.path.join(_TESTDATA_DIR, 'wrongversion.json'),
             "missingkey"   : os.path.join(_TESTDATA_DIR, 'missingkey.json'),
             "dummy_10_3_int16"   : os.path.join(_TESTDATA_DIR, 'dummy_10_3_int16.json'),
        }


class TestWrongVersion(unittest.TestCase):
    """ Test that a file with a wrong version raises an exception """
    def test_exception(self):
        with open(TESTDATA["wrongversion"]) as file:
            with self.assertRaises(AssertionError) as context:
                data = json.load(file)
                io_metadata.read_data(data) # This should trigger an exception

            self.assertTrue("TSDF file version" in str(context.exception), 
            "Wrong version is not being detected")

class TestTestMissingKey(unittest.TestCase):
    """ Test that a file with a missing mandatory key raises an exception """
    def test_exception(self):
        with open(TESTDATA["missingkey"]) as file:
            with self.assertRaises(AssertionError) as context:
                data = json.load(file)
                io_metadata.read_data(data) # This should trigger an exception

            self.assertTrue("missing key 'endianness'" in str(context.exception),
            f"Missing key is not being detected")

class TestParsing(unittest.TestCase):
    """ Test whether the TSDF objects are well specified are well defined. """
    def test_one_level_structure(self):
       with open(TESTDATA["hierarchical"]) as file:
        data = json.load(file)
        io_metadata.read_data(data) # This should trigger an exception
