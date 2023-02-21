import os
import unittest
import numpy as np
from tsdf import io, io_metadata

TESTDATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TESTDATA_FILES = {
    "flat": os.path.join(TESTDATA_DIR, "flat.json"),
    "hierarchical": os.path.join(TESTDATA_DIR, "hierarchical.json"),
    "wrongversion": os.path.join(TESTDATA_DIR, "wrongversion.json"),
    "missingkey": os.path.join(TESTDATA_DIR, "missingkey.json"),
    "dummy_10_3_int16": os.path.join(TESTDATA_DIR, "dummy_10_3_int16.json"),
}


class TestMetadataFileReading(unittest.TestCase):
    """Test loading of the metadata file."""

    def test_load_json_file(self):
        """Test that a json file gets loaded"""
        with open(TESTDATA_FILES["hierarchical"], "r") as file:
            data = io.load_file(file)
            self.assertEqual(len(data), 4)

    def test_load_json_path(self):
        """Test that a json file from a path gets loaded"""
        data = io.load_from_path(TESTDATA_FILES["hierarchical"])
        self.assertEqual(len(data), 4)

    def test_load_json_string(self):
        """Test that a json object gets loaded"""
        with open(TESTDATA_FILES["hierarchical"], "r") as file:
            json_string = file.read()
            data = io.load_string(json_string)
            self.assertEqual(len(data), 4)


class TestBinaryFileReading(unittest.TestCase):
    """Test reading of binary files based on the TSDF metadata."""

    def test_load_binary_float32(self):
        path = os.path.join(TESTDATA_DIR, "dummy_10_3_float32.json")
        metadata = io.load_from_path(path)
        data = io.load_binary_from_metadata(
            TESTDATA_DIR, io_metadata.get_file_metadata_at_index(metadata, 0)
        )
        self.assertEqual(data.shape, (10, 3))
        self.assertEqual(data.dtype, "float32")

    def test_load_binary_float64(self):
        path = os.path.join(TESTDATA_DIR, "dummy_10_3_float64.json")
        metadata = io.load_from_path(path)
        data = io.load_binary_from_metadata(
            TESTDATA_DIR, io_metadata.get_file_metadata_at_index(metadata, 0)
        )
        self.assertEqual(data.shape, (10, 3))
        self.assertEqual(data.dtype, "float64")

    def test_load_binary_float64_fail(self):
        """Should raise an exception on reading binary data"""
        path = os.path.join(TESTDATA_DIR, "dummy_10_3_float64_fail.json")
        metadata = io.load_from_path(path)
        with self.assertRaises(Exception) as exc_context:
            io.load_binary_from_metadata(
                TESTDATA_DIR, io_metadata.get_file_metadata_at_index(metadata, 0)
            )
        self.assertEqual(
            exc_context.exception.args[0], "Number of rows doesn't match file length."
        )

    def test_load_binary_int16(self):
        path = os.path.join(TESTDATA_DIR, "dummy_10_3_int16.json")
        metadata = io.load_from_path(path)
        data = io.load_binary_from_metadata(
            TESTDATA_DIR, io_metadata.get_file_metadata_at_index(metadata, 0)
        )
        self.assertEqual(data.shape, (10, 3))
        self.assertEqual(data.dtype, "int16")

    def test_load_like_ppp(self):
        path = os.path.join(TESTDATA_DIR, "like_ppp.json")
        metadata = io.load_from_path(path)
        time_data = io.load_binary_from_metadata(
            TESTDATA_DIR, io_metadata.get_file_metadata_at_index(metadata, 0)
        )
        self.assertEqual(time_data.shape, (17,))
        self.assertEqual(time_data.dtype, "float32")
        sample_data = io.load_binary_from_metadata(
            TESTDATA_DIR, io_metadata.get_file_metadata_at_index(metadata, 1)
        )
        self.assertEqual(sample_data.shape, (17, 6))
        self.assertEqual(sample_data.dtype, "int16")


class TestBinaryFileWriting(unittest.TestCase):
    """Test writing of binary files from loaded data (e.g., NumPy array)."""

    def test_save_binary(self):
        path = os.path.join(TESTDATA_DIR, "test_output_1.bin")
        rs = np.random.RandomState(seed=42)
        data = rs.rand(17, 1).astype(np.float32)
        io.save_binary_file(path, data)

        # Read file again to check contents
        with open(path, "rb") as fid:
            data2 = np.fromfile(fid, dtype="<f4")
            data2 = data2.reshape(17, 1)
            self.assertTrue(np.array_equal(data, data2))


class TestMetadataFileWriting(unittest.TestCase):
    """Test writing of metadata files based on loaded data."""

    def test_save_binary(self):
        path = os.path.join(TESTDATA_DIR, "test_output_1.bin")
        rs = np.random.RandomState(seed=42)
        data = rs.rand(17, 1).astype(np.float32)
        io.save_binary_file(path, data)

        # Read file again to check contents
        with open(path, "rb") as fid:
            data2 = np.fromfile(fid, dtype="<f4")
            data2 = data2.reshape(17, 1)
            self.assertTrue(np.array_equal(data, data2))
