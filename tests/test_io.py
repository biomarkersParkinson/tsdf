from tsdf import io
import os
import unittest

from tsdf.tsdf_metadata import TSDFMetadata

TESTDATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
TESTDATA_FILES = { "flat"         : os.path.join(TESTDATA_DIR, 'flat.json'),
             "hierarchical" : os.path.join(TESTDATA_DIR, 'hierarchical.json'),
             "wrongversion" : os.path.join(TESTDATA_DIR, 'wrongversion.json'),
             "missingkey"   : os.path.join(TESTDATA_DIR, 'missingkey.json'),
             "dummy_10_3_int16"   : os.path.join(TESTDATA_DIR, 'dummy_10_3_int16.json'),
        }



class TestFileReading(unittest.TestCase):
    def test_load_json_file(self):
        """ Test that a json file gets loaded """
        with open(TESTDATA_FILES["hierarchical"]) as file:
            data = io.load_file(file) # This should not trigger an exception
            self.assertEqual(len(data), 4)

    def test_load_json_path(self):
        """ Test that a json file from a path gets loaded """
        data = io.load_from_path(TESTDATA["hierarchical"]) # This should not trigger an exception   
        self.assertEqual(len(data), 4)

    def test_load_json_string(self):
        """ Test that a json object gets loaded """
        with open(TESTDATA_FILES["hierarchical"]) as file:
            json_string = file.read()
            data = io.load_string(json_string) # This should not trigger an exception   
            self.assertEqual(len(data), 4)

    def test_load_binary_float32(self):
        path = os.path.join(TESTDATA_DIR, 'dummy_10_3_float32.json')
        metadata = io.load_from_path(path)
        data = io.load_binary_from_metadata(TESTDATA_DIR, self.getFirstStream(metadata, 0))
        self.assertEqual(data.shape, (10, 3))
        self.assertEqual(data.dtype, 'float32')

    def test_load_binary_float64(self):
        path = os.path.join(TESTDATA_DIR, 'dummy_10_3_float64.json')
        metadata = io.load_from_path(path)
        
        data = io.load_binary_from_metadata(TESTDATA_DIR, self.getFirstStream(metadata, 0))
        self.assertEqual(data.shape, (10, 3))
        self.assertEqual(data.dtype, 'float64')

    def test_load_binary_float64_fail(self):
        """ Should raise an exception on reading binary data """
        path = os.path.join(TESTDATA_DIR, 'dummy_10_3_float64_fail.json')
        metadata = io.load_from_path(path)
        with self.assertRaises(Exception) as exc_context:
            io.load_binary_from_metadata(TESTDATA_DIR, self.getFirstStream(metadata, 0))
        self.assertEqual(exc_context.exception.args[0], "number of rows doesn't match file length")

    def test_load_binary_int16(self):
        path = os.path.join(TESTDATA_DIR, 'dummy_10_3_int16.json')
        metadata = io.load_from_path(path)
        data = io.load_binary_from_metadata(TESTDATA_DIR, self.getFirstStream(metadata, 0))
        self.assertEqual(data.shape, (10, 3))
        self.assertEqual(data.dtype, 'int16')

    def test_like_ppp(self):
        path = os.path.join(TESTDATA_DIR, 'like_ppp.json')
        metadata = io.load_from_path(path)
        time_data = io.load_binary_from_metadata(_TESTDATA_DIR, metadata[0])
        self.assertEqual(time_data.shape, (17,))
        self.assertEqual(time_data.dtype, 'float32')
        sample_data = io.load_binary_from_metadata(TESTDATA_DIR, self.getFirstStream(metadata, 1))
        self.assertEqual(sample_data.shape, (17, 6))
        self.assertEqual(sample_data.dtype, 'int16')


    def getFirstStream(self, metadata:dict, index:int) -> TSDFMetadata:
        """ Returns the metadata object at the position defined by the index."""
        for key, value in metadata.items():
            if(index == 0):
                return value
            index -= 1