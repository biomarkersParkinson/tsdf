import unittest
from tsdf.constants import TestConstants as CONST
from tsdf.load_tsdf import (
    load_metadata_file,
    load_metadata_from_path,
    load_metadata_string,
    load_metadatas_from_dir,
    load_metadata_legacy_file
)

class TestMetadataFileReading(unittest.TestCase):
    """Test loading of the metadata file."""

    def test_load_metadata_file(self):
        """Test that a json file gets loaded correctly."""
        with open(CONST.TEST_DATA_FILES["hierarchical"], "r") as file:
            data = load_metadata_file(file)
            self.assertEqual(len(data), 4)

    def test_load_metadata_legacy_file(self):
        """Test that a json file gets loaded correctly."""
        with open(CONST.TEST_DATA_FILES["legacy"], "r") as file:
            data = load_metadata_legacy_file(file)
            self.assertEqual(len(data), 2)

    def test_load_metadata_from_path(self):
        """Test that a json file from a path gets loaded correctly."""
        data = load_metadata_from_path(CONST.TEST_DATA_FILES["hierarchical"])
        self.assertEqual(len(data), 4)

    def test_load_metadata_string(self):
        """Test that a json object gets loaded from a string correctly."""
        with open(CONST.TEST_DATA_FILES["hierarchical"], "r") as file:
            json_string = file.read()
            data = load_metadata_string(json_string)
            self.assertEqual(len(data), 4)

    def test_load_metadatas_from_dir(self):
        """Test that all metadata files gets loaded from a directory correctly."""
        data = load_metadatas_from_dir(CONST.TEST_DATA_DIR)
        self.assertEqual(len(data), 6)
