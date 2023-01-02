from tsdf import io
import os
import unittest

TESTDATA = {
    "hierarchical" : os.path.join(os.path.dirname(__file__), 'data', 'hierarchical.json')
}

TESTDATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

class TestFileReading(unittest.TestCase):
    def test_load_json_file(self):
        """ Test that a json file gets loaded """
        with open(TESTDATA["hierarchical"]) as file:    
            data = io.load_file(file) # This should not trigger an exception
            self.assertGreater(len(data), 0)

    def test_load_json_path(self):
        """ Test that a json file from a path gets loaded """
        data = io.load_from_path(TESTDATA["hierarchical"]) # This should not trigger an exception   
        self.assertGreater(len(data), 0)

    def test_load_json_string(self):
        """ Test that a json object gets loaded """
        with open(TESTDATA["hierarchical"]) as file:
            json_string = file.read()
            data = io.load_string(json_string) # This should not trigger an exception   
            self.assertGreater(len(data), 0)

    def test_load_binary_from_metadata(self):
        path = os.path.join(TESTDATA_DIR, 'dummy_10_3_int16.json')
        metadata = io.load_from_path(path)
        data = io.load_binary_from_metadata(TESTDATA_DIR, metadata[0])
        assert data.shape == (10, 3)
        assert data.dtype == 'int16'
