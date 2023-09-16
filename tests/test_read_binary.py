import os
import unittest
import numpy as np
from tsdf.constants import TestConstants as CONST
from tsdf import read_tsdf
from tsdf import read_binary
from tsdf import parse_metadata


def load_single_bin_file(dir_path: str, file_name: str) -> np.ndarray:
    """
    Load a single binary file from the given directory path and file name.

    :param dir_path: The directory path where the binary file is located.
    :param file_name: The name of the binary file without the extension.

    :returns: The binary data as a numpy array.
    """
    path = os.path.join(dir_path, file_name + CONST.METADATA_EXTENSION)
    metadata = read_tsdf.load_metadata_from_path(path)
    data = read_binary.load_binary_from_metadata(
        dir_path, metadata[file_name + CONST.BINARY_EXTENSION]
    )
    return data


class TestBinaryFileReading(unittest.TestCase):
    """Test reading of binary files based on the TSDF metadata."""

    def test_load_binary_float32(self):
        data = load_single_bin_file(CONST.TEST_DATA_DIR, "example_10_3_float32")

        self.assertEqual(data.shape, (10, 3))
        self.assertEqual(data.dtype, "float32")

    def test_load_binary_float64(self):
        data = load_single_bin_file(CONST.TEST_DATA_DIR, "example_10_3_float64")

        self.assertEqual(data.shape, (10, 3))
        self.assertEqual(data.dtype, "float64")

    # def test_load_binary_float64_fail(self):
    #     """Should raise an exception on reading binary data"""
    #     path = os.path.join(CONST.TEST_DATA_DIR, "example_10_3_float64_meta_fail.json")
    #     metadata = load_tsdf.load_metadata_from_path(path)
    #     with self.assertRaises(Exception) as exc_context:
    #         io_binary.load_binary_from_metadata(
    #             CONST.TEST_DATA_DIR, io_metadata.get_file_metadata_at_index(metadata, 0)
    #         )
    #     self.assertEqual(
    #         exc_context.exception.args[0], "Number of rows doesn't match file length."
    #     )

    def test_load_binary_int16(self):
        data = load_single_bin_file(CONST.TEST_DATA_DIR, "example_10_3_int16")

        self.assertEqual(data.shape, (10, 3))
        self.assertEqual(data.dtype, "int16")

    def test_load_like_ppp(self):
        path = CONST.TEST_DATA_FILES["ppp"]
        metadata = read_tsdf.load_metadata_from_path(path)
        time_data = read_binary.load_binary_from_metadata(
            CONST.TEST_DATA_DIR, parse_metadata.get_file_metadata_at_index(metadata, 0)
        )
        self.assertEqual(time_data.shape, (17,))
        # time data should be loaded as float64
        self.assertEqual(time_data.dtype, "float32")

        sample_data = read_binary.load_binary_from_metadata(
            CONST.TEST_DATA_DIR, parse_metadata.get_file_metadata_at_index(metadata, 1)
        )
        self.assertEqual(sample_data.shape, (17, 6))
        # sample data should be loaded as int16
        self.assertEqual(sample_data.dtype, "int16")

    def test_random_access(self):
        # TODO: test the new random access functionality
        file_name = "example_10_3_int16"
        path = os.path.join(CONST.TEST_DATA_DIR, file_name + CONST.METADATA_EXTENSION)
        metadata = read_tsdf.load_metadata_from_path(path)
        data = read_binary.load_binary_from_metadata(
            CONST.TEST_DATA_DIR,
            metadata[file_name + CONST.BINARY_EXTENSION],
            2,
            6,
        )
        self.assertEqual(data.shape, (4, 3))
        self.assertEqual(data.dtype, "int16")
