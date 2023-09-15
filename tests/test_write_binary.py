import os
import unittest
import numpy as np
from tsdf.constants import TestConstants as CONST
from tsdf import read_tsdf
from tsdf import write_binary



class TestBinaryFileWriting(unittest.TestCase):
    """Test writing of binary files from loaded data (e.g., NumPy array)."""

    def test_write_binary(self):
        """Save a NumPy array as a binary file."""
        test_file_name = "tmp_test_output_1.bin"
        rs = np.random.RandomState(seed=42)
        data_original = rs.rand(17, 1).astype(np.float32)
        with open(CONST.TEST_DATA_FILES["flat"], "r") as file:
            metadatas = read_tsdf.load_metadata_file(file)
            write_binary.write_binary_file(
                CONST.TEST_OUTPUT_DATA_DIR,
                test_file_name,
                data_original,
                metadatas["audio_voice_089.raw"].get_plain_tsdf_dict_copy(),
            )

        # Read file again to check contents
        path = os.path.join(CONST.TEST_OUTPUT_DATA_DIR, test_file_name)
        with open(path, "rb") as fid:
            data_written = np.fromfile(fid, dtype="<f4")
            data_written = data_written.reshape(17, 1)
            self.assertTrue(np.array_equal(data_original, data_written))
