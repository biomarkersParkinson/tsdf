import os
import unittest
import numpy as np
from tsdf import io, io_metadata, tsdf_metadata

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
            data = io.load_metadata_file(file)
            self.assertEqual(len(data), 4)

    def test_load_json_path(self):
        """Test that a json file from a path gets loaded"""
        data = io.load_metadata_from_path(TESTDATA_FILES["hierarchical"])
        self.assertEqual(len(data), 4)

    def test_load_json_string(self):
        """Test that a json object gets loaded"""
        with open(TESTDATA_FILES["hierarchical"], "r") as file:
            json_string = file.read()
            data = io.load_metadata_string(json_string)
            self.assertEqual(len(data), 4)


def load_single_bin_file(dir: str, file_name: str) -> np.ndarray:
    path = os.path.join(dir, file_name + ".json")
    metadata = io.load_metadata_from_path(path)
    data = io.load_binary_from_metadata(dir, metadata[file_name + ".bin"])
    return data


class TestBinaryFileReading(unittest.TestCase):
    """Test reading of binary files based on the TSDF metadata."""

    def test_load_binary_float32(self):
        data = load_single_bin_file(TESTDATA_DIR, "dummy_10_3_float32")

        self.assertEqual(data.shape, (10, 3))
        self.assertEqual(data.dtype, "float32")

    def test_load_binary_float64(self):
        data = load_single_bin_file(TESTDATA_DIR, "dummy_10_3_float64")

        self.assertEqual(data.shape, (10, 3))
        self.assertEqual(data.dtype, "float64")

    def test_load_binary_float64_fail(self):
        """Should raise an exception on reading binary data"""
        path = os.path.join(TESTDATA_DIR, "dummy_10_3_float64_fail.json")
        metadata = io.load_metadata_from_path(path)
        with self.assertRaises(Exception) as exc_context:
            io.load_binary_from_metadata(
                TESTDATA_DIR, io_metadata.get_file_metadata_at_index(metadata, 0)
            )
        self.assertEqual(
            exc_context.exception.args[0], "Number of rows doesn't match file length."
        )

    def test_load_binary_int16(self):
        data = load_single_bin_file(TESTDATA_DIR, "dummy_10_3_int16")

        self.assertEqual(data.shape, (10, 3))
        self.assertEqual(data.dtype, "int16")

    def test_load_like_ppp(self):
        path = os.path.join(TESTDATA_DIR, "like_ppp.json")
        metadata = io.load_metadata_from_path(path)
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

    def test_write_binary(self):
        """Save a NumPy array as a binary file."""
        test_file_name = "tmp_test_output_1.bin"
        rs = np.random.RandomState(seed=42)
        data = rs.rand(17, 1).astype(np.float32)
        with open(TESTDATA_FILES["flat"], "r") as file:
            metadatas = io.load_metadata_file(file)
            io.write_binary_file(
                TESTDATA_DIR,
                test_file_name,
                data,
                metadatas["audio_voice_089.raw"].get_plain_tsdf_dict_copy(),
            )

        # Read file again to check contents
        path = os.path.join(TESTDATA_DIR, test_file_name)
        with open(path, "rb") as fid:
            data2 = np.fromfile(fid, dtype="<f4")
            data2 = data2.reshape(17, 1)
            self.assertTrue(np.array_equal(data, data2))


class TestMetadataFileWriting(unittest.TestCase):
    """Test writing of metadata files based on loaded data."""

    def test_save_metadata(self):
        """Test writing multiple binary files and combining their TSDF metadatas."""
        test_name = "tmp_test_save_metadata"
        rs = np.random.RandomState(seed=42)
        data_1 = rs.rand(17, 1).astype(np.float32)
        data_2 = rs.rand(15, 2).astype(np.int16)
        data_3 = rs.rand(10, 3).astype(np.int16)

        use_case_name = "dummy_10_3_int16"
        path = TESTDATA_FILES[use_case_name]
        loaded_meta: tsdf_metadata.TSDFMetadata = io.load_metadata_from_path(path)[
            use_case_name + ".bin"
        ]

        new_meta_1 = io.write_binary_file(
            TESTDATA_DIR,
            test_name + "_1.bin",
            data_1,
            loaded_meta.get_plain_tsdf_dict_copy(),
        )
        new_meta_2 = io.write_binary_file(
            TESTDATA_DIR,
            test_name + "_2.bin",
            data_2,
            loaded_meta.get_plain_tsdf_dict_copy(),
        )

        new_meta_3 = io.write_binary_file(
            TESTDATA_DIR,
            test_name + "_3.bin",
            data_3,
            loaded_meta.get_plain_tsdf_dict_copy(),
        )

        # Combine two TSDF files
        io.write_metadata([new_meta_1, new_meta_2, new_meta_3], test_name + ".json")

        # Read the written metadata

        meta = io.load_metadata_from_path(
            os.path.join(TESTDATA_DIR, test_name + ".json")
        )
        self.assertEqual(len(meta), 3)
        self.assertEqual(meta[test_name + "_1.bin"].rows, 17)
        self.assertEqual(meta[test_name + "_2.bin"].rows, 15)
        self.assertEqual(meta[test_name + "_3.bin"].rows, 10)

    def test_bin_processing_and_writing_metadata(self):
        """Test binary file reading, processing, and writing of the new binary and metadata files."""
        # Load existing TSDF metadata and the corresponding binary data
        file_name = "dummy_10_3_int16"
        path = os.path.join(TESTDATA_DIR, file_name + ".json")
        original_metadata = io.load_metadata_from_path(path)[file_name + ".bin"]
        original_data = io.load_binary_from_metadata(TESTDATA_DIR, original_metadata)

        # Perform light data processing
        new_data = (original_data / 10).astype("float32")

        # Write new binary file
        new_file_name = "tmp_test_dummy_10_3_int16_to_float32"
        new_metadata = io.write_binary_file(
            TESTDATA_DIR,
            new_file_name + ".bin",
            new_data,
            original_metadata.get_plain_tsdf_dict_copy(),
        )

        # Write the new metadata file
        io.write_metadata([new_metadata], new_file_name + ".json")

        # Read file again to check contents
        final_data = load_single_bin_file(TESTDATA_DIR, new_file_name)
        self.assertEqual(final_data.shape, (10, 3))
        self.assertEqual(final_data.dtype, "float32")
