import json
import pytest
from tsdf import parse_metadata
from tsdf.tsdfmetadata import TSDFMetadataFieldError, TSDFMetadataFieldValueError


def test_load_wrong_version(shared_datadir):
    """Test that a file with a wrong version raises an exception."""
    
    path = shared_datadir / "wrongversion_meta_fail.json"
    with open(path, "r") as file:
        data = json.load(file)
        with pytest.raises(TSDFMetadataFieldValueError):
            parse_metadata.read_data(data, path) # This should trigger an exception

def test_load_missing_key(shared_datadir):
    """Test that a file with a missing mandatory key raises an exception."""

    path = shared_datadir / "missingkey_meta_fail.json"
    with open(path, "r") as file:
        data = json.load(file)
        with pytest.raises(TSDFMetadataFieldError):
            parse_metadata.read_data(data, path)  # This should trigger an exception


def test_load_flat_structure(shared_datadir):
    """Test parsing of a flat TSDF metadata file."""

    path = shared_datadir / "flat_meta.json"
    with open(path, "r") as file:
        data = json.load(file)
        streams = parse_metadata.read_data(data, path)
        first_stream = parse_metadata.get_file_metadata_at_index(streams, 0)
        version: str = first_stream.metadata_version
    for key, value in data.items():
        if parse_metadata.is_mandatory_type(key, version):
            assert(value == first_stream.__getattribute__(key))
