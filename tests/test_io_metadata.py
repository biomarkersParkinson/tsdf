import json
import os
import unittest
from tsdf import io_metadata
from tsdf.tsdf_metadata import TSDFMetadataFieldError, TSDFMetadataFieldValueError

TESTDATA_DIR = os.path.join(os.path.dirname(__file__), "data")
TESTDATA = {
    "flat": os.path.join(TESTDATA_DIR, "flat_meta.json"),
    "hierarchical": os.path.join(TESTDATA_DIR, "hierarchical_meta.json"),
    "wrongversion": os.path.join(TESTDATA_DIR, "wrongversion_meta_fail.json"),
    "missingkey": os.path.join(TESTDATA_DIR, "missingkey_meta_fail.json"),
}


class TestWrongFormatting(unittest.TestCase):
    """Test whether the exceptions are thrown in case the metadata file is not well annotated."""

    def test_load_wrong_version(self):
        """Test that a file with a wrong version raises an exception."""
        path = TESTDATA["wrongversion"]
        with open(path, "r") as file:
            with self.assertRaises(TSDFMetadataFieldValueError) as context:
                data = json.load(file)
                io_metadata.read_data(data, path)  # This should trigger an exception

    def test_load_missing_key(self):
        """Test that a file with a missing mandatory key raises an exception."""
        path = TESTDATA["missingkey"]
        with open(path, "r") as file:
            with self.assertRaises(TSDFMetadataFieldError) as context:
                data = json.load(file)
                io_metadata.read_data(data, path)  # This should trigger an exception


class TestTSDFMetadataParsing(unittest.TestCase):
    """Test whether the TSDF objects are well specified are well defined."""

    def test_load_flat_structure(self):
        """Test parsing of a flat TSDF metadata file."""
        path = TESTDATA["flat"]
        with open(path, "r") as file:
            data = json.load(file)
            streams = io_metadata.read_data(data, path)
            first_stream = io_metadata.get_file_metadata_at_index(streams, 0)
            version: str = first_stream.metadata_version
        for key, value in data.items():
            if io_metadata.is_mandatory_type(key, version):
                self.assertTrue(value == first_stream.__getattribute__(key))
