from tsdf.io import load
import os
import unittest

TESTDATA = { "flat"         : os.path.join(os.path.dirname(__file__), 'data/flat.json'),
             "hierarchical" : os.path.join(os.path.dirname(__file__), 'data/hierarchical.json'),
             "wrongversion" : os.path.join(os.path.dirname(__file__), 'data/wrongversion.json'),
             "missingkey"   : os.path.join(os.path.dirname(__file__), 'data/missingkey.json'),
        }

def test_flat():
    """ Test that a flat json gets loaded """
    with open(TESTDATA["flat"]) as file:
        data = load(file)

def test_hierarchical():
    """ Test that the hierarchical json gets loaded """
    with open(TESTDATA["hierarchical"]) as file:
        data = load(file)

class TestWrongVersion(unittest.TestCase):
    """ Test that a file with a wrong version raises an exception """
    def test_exception(self):
        with open(TESTDATA["wrongversion"]) as file:
            with self.assertRaises(AssertionError) as context:
                data = load(file) # This should trigger an exception

            self.assertTrue("TSDF file version" in str(context.exception), 
            f"Wrong version is not being detected")

class TestTestMissingKey(unittest.TestCase):
    """ Test that a file with a missing mandatory key raises an exception """
    def test_exception(self):
        with open(TESTDATA["missingkey"]) as file:
            with self.assertRaises(AssertionError) as context:
                data = load(file) # This should trigger an exception

            self.assertTrue("Missing key: endianness" in str(context.exception),
            f"Missing key is not being detected")