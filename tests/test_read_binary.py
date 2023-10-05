import numpy as np
from pathlib import Path
import tsdf
from tsdf import parse_metadata
from utils import load_single_bin_file


def test_load_binary_float32(shared_datadir):
    data = load_single_bin_file(shared_datadir, "example_10_3_float32")
    assert(data.shape == (10, 3))
    assert(data.dtype == "float32")

def test_load_binary_float64(shared_datadir):
    data = load_single_bin_file(shared_datadir, "example_10_3_float64")
    assert(data.shape == (10, 3))
    assert(data.dtype == "float64")

# def test_load_binary_float64_fail(shared_datadir):
#     """Should raise an exception on reading binary data"""
#     path = shared_datadir / "example_10_3_float64_meta_fail.json"
#     metadata = load_tsdf.load_metadata_from_path(path)
#     with self.assertRaises(Exception) as exc_context:
#         io_binary.load_binary_from_metadata(
#             shared_datadir, io_metadata.get_file_metadata_at_index(metadata, 0)
#         )
#     assert(exc_context.exception.args[0] == "Number of rows doesn't match file length.")

def test_load_binary_int16(shared_datadir):
    data = load_single_bin_file(shared_datadir, "example_10_3_int16")
    assert(data.shape == (10, 3))
    assert(data.dtype == "int16")

def test_load_like_ppp(shared_datadir):
    metadata = tsdf.load_metadata_from_path(shared_datadir / "ppp_format_meta.json")
    time_data = tsdf.load_binary_from_metadata(parse_metadata.get_file_metadata_at_index(metadata, 0))
    assert(time_data.shape == (17,))
    # time data should be loaded as float64
    assert(time_data.dtype == "float32")

    sample_data = tsdf.load_binary_from_metadata(parse_metadata.get_file_metadata_at_index(metadata, 1))
    assert(sample_data.shape == (17, 6))
    # sample data should be loaded as int16
    assert(sample_data.dtype == "int16")

def test_random_access(shared_datadir):
    # TODO: test the new random access functionality
    name = "example_10_3_int16"
    metadata = tsdf.load_metadata_from_path(shared_datadir / (name + "_meta.json"))
    data = tsdf.load_binary_from_metadata(metadata[name + ".bin"], 2, 6)
    assert(data.shape == (4, 3))
    assert(data.dtype == "int16")
