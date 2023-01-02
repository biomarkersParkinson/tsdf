import json
import os
import unittest

from tsdf.tsdf_metadata import TSDFMetadata

TESTDATA = { "flat"         : os.path.join(os.path.dirname(__file__), 'data/flat.json'),
             "hierarchical" : os.path.join(os.path.dirname(__file__), 'data/hierarchical.json'),
             "wrongversion" : os.path.join(os.path.dirname(__file__), 'data/wrongversion.json'),
             "missingkey"   : os.path.join(os.path.dirname(__file__), 'data/missingkey.json'),
        }


class TestWrongVersion(unittest.TestCase):
    """ Test that a file with a wrong version raises an exception """
    def test_exception(self):
        with open(TESTDATA["wrongversion"]) as file:
            with self.assertRaises(AssertionError) as context:
                data = json.load(file)
                TSDFMetadata.read_data(data) # This should trigger an exception

            self.assertTrue("TSDF file version" in str(context.exception), 
            "Wrong version is not being detected")

class TestTestMissingKey(unittest.TestCase):
    """ Test that a file with a missing mandatory key raises an exception """
    def test_exception(self):
        with open(TESTDATA["missingkey"]) as file:
            with self.assertRaises(AssertionError) as context:
                data = json.load(file)
                TSDFMetadata.read_data(data) # This should trigger an exception

            self.assertTrue("missing key 'endianness'" in str(context.exception),
            f"Missing key is not being detected")

class TestParsing(unittest.TestCase):
    """ Test whether the JSON metadata file is well formatted """
    def test_metadata_format(self):
       with open(TESTDATA["hierarchical"]) as file:
        data = json.load(file)
        TSDFMetadata.read_data(data) # This should trigger an exception
