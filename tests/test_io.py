from tsdf import io
import os
import unittest

TESTDATA = {"hierarchical" : os.path.join(os.path.dirname(__file__), 'data/hierarchical.json') }

class TestFileReading(unittest.TestCase):
    """ Test that a json file gets loaded """
    def test_load_json_file(self):
        with open(TESTDATA["hierarchical"]) as file:    
            data = io.load_file(file) # This should not trigger an exception
            self.assertGreater(len(data), 0)

    """ Test that a json file from a path gets loaded """
    def test_load_json_path(self):
        data = io.load_from_path(TESTDATA["hierarchical"]) # This should not trigger an exception   
        self.assertGreater(len(data), 0)

    """ Test that a json object gets loaded """
    def test_load_json_string(self):
        with open(TESTDATA["hierarchical"]) as file:
            json_string = file.read()
            data = io.load_string(json_string) # This should not trigger an exception   
            self.assertGreater(len(data), 0)