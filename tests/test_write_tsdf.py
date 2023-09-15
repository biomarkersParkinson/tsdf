import os
import unittest
import numpy as np
from tsdf import read_tsdf
from tsdf.constants import TestConstants as CONST
from tsdf.read_tsdf import (
    load_metadata_from_path
)
from tsdf import read_binary, read_tsdf
from tsdf import write_binary, write_tsdf
from tsdf.tsdfmetadata import TSDFMetadata

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

class TestMetadataFileWriting(unittest.TestCase):
    """Test writing of metadata files based on loaded data."""

    def test_save_metadata(self):
        """Test writing multiple binary files and combining their TSDF metadatas."""
        test_name = "tmp_test_save_metadata"
        rs = np.random.RandomState(seed=42)
        data_1 = rs.rand(17, 1).astype(np.float32)
        data_2 = rs.rand(15, 2).astype(np.int16)
        data_3 = rs.rand(10, 3).astype(np.int16)

        use_case_name = "example_10_3_int16"
        path = CONST.TEST_DATA_FILES[use_case_name]
        loaded_meta: TSDFMetadata = load_metadata_from_path(path)[
            use_case_name + CONST.BINARY_EXTENSION
        ]

        new_meta_1 = write_binary.write_binary_file(
            CONST.TEST_OUTPUT_DATA_DIR,
            test_name + "_1.bin",
            data_1,
            loaded_meta.get_plain_tsdf_dict_copy(),
        )
        new_meta_2 = write_binary.write_binary_file(
            CONST.TEST_OUTPUT_DATA_DIR,
            test_name + "_2.bin",
            data_2,
            loaded_meta.get_plain_tsdf_dict_copy(),
        )

        new_meta_3 = write_binary.write_binary_file(
            CONST.TEST_OUTPUT_DATA_DIR,
            test_name + "_3.bin",
            data_3,
            loaded_meta.get_plain_tsdf_dict_copy(),
        )

        # Combine two TSDF files
        write_tsdf.write_metadata(
            [new_meta_1, new_meta_2, new_meta_3],
            test_name + CONST.METADATA_EXTENSION,
        )

        # Read the written metadata

        meta = load_metadata_from_path(
            os.path.join(
                CONST.TEST_OUTPUT_DATA_DIR, test_name + CONST.METADATA_EXTENSION
            )
        )
        self.assertEqual(len(meta), 3)
        self.assertEqual(meta[test_name + "_1.bin"].rows, 17)
        self.assertEqual(meta[test_name + "_2.bin"].rows, 15)
        self.assertEqual(meta[test_name + "_3.bin"].rows, 10)

    def test_bin_processing_and_writing_metadata(self):
        """Test binary file reading, processing, and writing of the new binary and metadata files."""
        # Load existing TSDF metadata and the corresponding binary data
        file_name = "example_10_3_int16"
        path = os.path.join(CONST.TEST_DATA_DIR, file_name + CONST.METADATA_EXTENSION)
        original_metadata = load_metadata_from_path(path)[
            file_name + CONST.BINARY_EXTENSION
        ]
        original_data = read_binary.load_binary_from_metadata(
            CONST.TEST_DATA_DIR, original_metadata
        )

        # Perform light data processing
        new_data = (original_data / 10).astype("float32")

        # Write new binary file
        new_file_name = "tmp_test_example_10_3_int16_to_float32"
        new_metadata = write_binary.write_binary_file(
            CONST.TEST_OUTPUT_DATA_DIR,
            new_file_name + CONST.BINARY_EXTENSION,
            new_data,
            original_metadata.get_plain_tsdf_dict_copy(),
        )

        # Write the new metadata file
        write_tsdf.write_metadata([new_metadata], new_file_name + CONST.METADATA_EXTENSION)

        # Read file again to check contents
        final_data = load_single_bin_file(CONST.TEST_OUTPUT_DATA_DIR, new_file_name)
        self.assertEqual(final_data.shape, (10, 3))
        self.assertEqual(final_data.dtype, "float32")
