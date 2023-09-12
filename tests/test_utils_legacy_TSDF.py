import os
import unittest
from tsdf import io
from tsdf.utils_legacy_tsdf import generate_tsdf_metadata_from_tsdb
from tsdf.constants import TestConstants as CONST


class TestConversion(unittest.TestCase):
    """Test whether the conversion from TSDB (legacy metadata format) to TSDF works."""

    def test_conversion(self):
        path_to_file = os.path.join(CONST.TEST_DATA_DIR, "ppp_format_meta_legacy.json")
        path_to_new_file = os.path.join(
            CONST.TEST_OUTPUT_DATA_DIR, "tmp_test_ppp_format_meta.json"
        )

        path_to_existing_tsdf_file = os.path.join(
            CONST.TEST_DATA_DIR, "ppp_format_meta.json"
        )

        # Generate a TSDF metadata file from TSDB
        generate_tsdf_metadata_from_tsdb(path_to_file, path_to_new_file)

        # Load the generated metadata file
        new_meta = io.load_metadata_from_path(path_to_new_file)

        # Load the existing metadata file
        existing_meta = io.load_metadata_from_path(path_to_existing_tsdf_file)

        # Compare the two metadata files (whether the mapped TSDFs fields are the same)
        self.assertEqual(
            new_meta["ppp_format_time.bin"].get_plain_tsdf_dict_copy(),
            existing_meta["ppp_format_time.bin"].get_plain_tsdf_dict_copy(),
        )

        self.assertEqual(
            new_meta["ppp_format_samples.bin"].get_plain_tsdf_dict_copy(),
            existing_meta["ppp_format_samples.bin"].get_plain_tsdf_dict_copy(),
        )
