from tsdf.io import load
import os
import unittest

TESTDATA = { "flat"         : os.path.join(os.path.dirname(__file__), 'data/flat.json'),
             "hierarchical" : os.path.join(os.path.dirname(__file__), 'data/hierarchical.json'),
             "wrongversion" : os.path.join(os.path.dirname(__file__), 'data/wrongversion.json'),
        }

def test_flat():
    with open(TESTDATA["flat"]) as file:
        data = load(file)

def test_hierarchical():
    with open(TESTDATA["hierarchical"]) as file:
        data = load(file)

class TestWrongVersion(unittest.TestCase):
    def test_exception(self):
        with open(TESTDATA["wrongversion"]) as file:
            with self.assertRaises(AssertionError) as context:
                data = load(file) # This should trigger an exception

            self.assertTrue("TSDF file version" in str(context.exception), 
            f"Wrong version is not being detected")
