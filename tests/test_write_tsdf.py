import os
import numpy as np
import pytest
import tsdf
from tsdf import TSDFMetadata
from tsdf.tsdfmetadata import TSDFMetadataFieldValueError
from utils import load_single_bin_file


def test_save_metadata(shared_datadir):
    """Test writing multiple binary files and combining their TSDF metadatas."""
    test_name = "tmp_test_save_metadata"
    rs = np.random.RandomState(seed=42)
    data_1 = rs.rand(17, 1).astype(np.float32)
    data_2 = rs.rand(15, 2).astype(np.int16)
    data_3 = rs.rand(10, 3).astype(np.int16)

    name = "example_10_3_int16"
    metas = tsdf.load_metadata_from_path(shared_datadir / (name + "_meta.json"))
    loaded_meta: TSDFMetadata = metas[name + ".bin"]

    new_meta_1 = tsdf.write_binary_file(
        shared_datadir,
        test_name + "_1.bin",
        data_1,
        loaded_meta.get_plain_tsdf_dict_copy(),
    )
    new_meta_2 = tsdf.write_binary_file(
        shared_datadir,
        test_name + "_2.bin",
        data_2,
        loaded_meta.get_plain_tsdf_dict_copy(),
    )

    new_meta_3 = tsdf.write_binary_file(
        shared_datadir,
        test_name + "_3.bin",
        data_3,
        loaded_meta.get_plain_tsdf_dict_copy(),
    )

    # Combine two TSDF files
    tsdf.write_metadata(
        [new_meta_1, new_meta_2, new_meta_3],
        test_name + "_meta.json",
    )

    # Read the written metadata
    meta = tsdf.load_metadata_from_path(shared_datadir / (test_name + "_meta.json"))

    assert len(meta) == 3
    assert meta[test_name + "_1.bin"].rows == 17
    assert meta[test_name + "_2.bin"].rows == 15
    assert meta[test_name + "_3.bin"].rows == 10


def test_bin_processing_and_writing_metadata(shared_datadir):
    """Test binary file reading, processing, and writing of the new binary and metadata files."""
    # Load existing TSDF metadata and the corresponding binary data
    name = "example_10_3_int16"
    metas = tsdf.load_metadata_from_path(shared_datadir / (name + "_meta.json"))
    original_metadata = metas[name + ".bin"]
    original_data = tsdf.load_ndarray_from_binary(original_metadata)

    # Perform light data processing
    new_data = (original_data / 10).astype("float32")

    # Write new binary file
    new_name = "tmp_test_example_10_3_int16_to_float32"
    new_metadata = tsdf.write_binary_file(
        shared_datadir,
        new_name + ".bin",
        new_data,
        original_metadata.get_plain_tsdf_dict_copy(),
    )

    # Write the new metadata file
    tsdf.write_metadata([new_metadata], new_name + "_meta.json")

    # Read file again to check contents
    final_data = load_single_bin_file(shared_datadir, new_name)
    assert final_data.shape == (10, 3)
    assert final_data.dtype == "float32"


def test_write_metadata_only(shared_datadir):
    """ Construct simple metadata from scratch and write it to a file. """
    # Define the metadata
    basic_metadata = {
        "subject_id": "example",
        "study_id": "example",
        "device_id": "example",
        "endianness": "little",
        "metadata_version": "0.1",
        "start_datetime_unix_ms": 1571135957025,
        "start_iso8601": "2019-10-15T10:39:17.025000+00:00", # not iso8601 format
        "end_datetime_unix_ms": 1571168851826,
        "end_iso8601": "2019-10-15T19:47:31.826000+00:00",
        "channels": ["x", "y", "z"],
        "units": ["m/s/s", "m/s/s", "m/s/s"],
        "data_type": "float",
        "bits": 32,
        "rows": 17,
        "file_name": "example_17_1_float32.bin",
    }
    metadata = TSDFMetadata(basic_metadata, shared_datadir)
    tsdf.write_metadata([metadata], "tmp_meta.json")
    assert os.path.exists(os.path.join(shared_datadir, "tmp_meta.json"))


def test_write_metadata_validate_fail(shared_datadir):
    """ Should fail on writing metadata with wrong date format. """
    # Define the metadata
    basic_metadata = {
        "subject_id": "example",
        "study_id": "example",
        "device_id": "example",
        "endianness": "little",
        "metadata_version": "0.1",
        "start_datetime_unix_ms": 1571135957025,
        "start_iso8601": "2019-10-15 10:39:17.025000+00:00", # not iso8601 format
        "end_datetime_unix_ms": 1571168851826,
        "end_iso8601": "2019-10-15T19:47:31.826000+00:00",
        "channels": ["x", "y", "z"],
        "units": ["m/s/s", "m/s/s", "m/s/s"],
        "data_type": "float",
        "bits": 32,
        "rows": 17,
        "file_name": "example_17_1_float32.bin",
    }
    metadata = TSDFMetadata(basic_metadata, shared_datadir, do_validate=False) # Should validate on write below
    with pytest.raises(TSDFMetadataFieldValueError):
        tsdf.write_metadata([metadata], "tmp_meta.json")
