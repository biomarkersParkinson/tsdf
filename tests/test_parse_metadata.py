import json
import unittest
from tsdf import parse_metadata
from tsdf.tsdfmetadata import TSDFMetadataFieldError, TSDFMetadataFieldValueError
from tsdf.constants import TestConstants as CONST


class TestWrongFormatting(unittest.TestCase):
    """Test whether the exceptions are thrown in case the metadata file is not well annotated."""

    def test_load_wrong_version(self):
        """Test that a file with a wrong version raises an exception."""
        path = CONST.TEST_DATA_FILES["wrongversion"]
        with open(path, "r") as file:
            with self.assertRaises(TSDFMetadataFieldValueError) as context:
                data = json.load(file)
                parse_metadata.read_data(data, path)  # This should trigger an exception

    def test_load_missing_key(self):
        """Test that a file with a missing mandatory key raises an exception."""
        path = CONST.TEST_DATA_FILES["missingkey"]
        with open(path, "r") as file:
            with self.assertRaises(TSDFMetadataFieldError) as context:
                data = json.load(file)
                parse_metadata.read_data(data, path)  # This should trigger an exception


class TestTSDFMetadataParsing(unittest.TestCase):
    """Test whether the TSDF objects are well specified are well defined."""

    def test_load_flat_structure(self):
        """Test parsing of a flat TSDF metadata file."""
        path = CONST.TEST_DATA_FILES["flat"]
        with open(path, "r") as file:
            data = json.load(file)
            streams = parse_metadata.read_data(data, path)
            first_stream = parse_metadata.get_file_metadata_at_index(streams, 0)
            version: str = first_stream.metadata_version
        for key, value in data.items():
            if parse_metadata.is_mandatory_type(key, version):
                self.assertTrue(value == first_stream.__getattribute__(key))
