import numpy as np
from pathlib import Path

import pandas as pd
import tsdf
from tsdf import parse_metadata
from tsdf.constants import ConcatenationType
from utils import load_single_bin_file


def test_load_binary_float32(shared_datadir):
    data = load_single_bin_file(shared_datadir, "example_10_3_float32")
    assert data.shape == (10, 3)
    assert data.dtype == "float32"


def test_load_binary_float64(shared_datadir):
    data = load_single_bin_file(shared_datadir, "example_10_3_float64")
    assert data.shape == (10, 3)
    assert data.dtype == "float64"


# def test_load_binary_float64_fail(shared_datadir):
#     """Should raise an exception on reading binary data"""
#     path = shared_datadir / "example_10_3_float64_meta_fail.json"
#     metadata = load_tsdf.load_metadata_from_path(path)
#     with self.assertRaises(Exception) as exc_context:
#         io_binary.load_ndarray_from_binary(
#             shared_datadir, io_metadata.get_file_metadata_at_index(metadata, 0)
#         )
#     assert(exc_context.exception.args[0] == "Number of rows doesn't match file length.")


def test_load_binary_int16(shared_datadir):
    data = load_single_bin_file(shared_datadir, "example_10_3_int16")
    assert data.shape == (10, 3)
    assert data.dtype == "int16"


def test_load_like_ppp(shared_datadir):
    metadata = tsdf.load_metadata_from_path(shared_datadir / "ppp_format_meta.json")
    time_data = tsdf.load_ndarray_from_binary(
        parse_metadata.get_file_metadata_at_index(metadata, 0)
    )
    assert time_data.shape == (17,)
    # time data should be loaded as float64
    assert time_data.dtype == "float32"

    sample_data = tsdf.load_ndarray_from_binary(
        parse_metadata.get_file_metadata_at_index(metadata, 1)
    )
    assert sample_data.shape == (17, 6)
    # sample data should be loaded as int16
    assert sample_data.dtype == "int16"


def test_random_access(shared_datadir):
    # TODO: test the new random access functionality
    name = "example_10_3_int16"
    metadata = tsdf.load_metadata_from_path(shared_datadir / (name + "_meta.json"))
    data = tsdf.load_ndarray_from_binary(metadata[name + ".bin"], 2, 6)
    assert data.shape == (4, 3)
    assert data.dtype == "int16"


def test_load_binary_to_dataframe(shared_datadir):
    metadata = tsdf.load_metadata_from_path(shared_datadir / "ppp_format_meta.json")
    df = tsdf.load_dataframe_from_binaries(
        [metadata["ppp_format_time.bin"], metadata["ppp_format_samples.bin"]],
        ConcatenationType.columns,
    )
    assert isinstance(df, pd.DataFrame), "Result should be a single pandas DataFrame"

    assert df.shape == (17, 7)
    assert df.columns.tolist() == [
        "time",
        "acceleration_x",
        "acceleration_y",
        "acceleration_z",
        "rotation_x",
        "rotation_y",
        "rotation_z",
    ]


def test_load_dataframe_concatenation_rows(shared_datadir):
    metadata = tsdf.load_metadata_from_path(
        shared_datadir / "hierarchical/hierarchical_meta.json"
    )
    df_accel = tsdf.load_dataframe_from_binaries(
        [metadata["accelerometer_t1.bin"], metadata["accelerometer_t2.bin"]],
        ConcatenationType.rows,
    )
    assert isinstance(
        df_accel, pd.DataFrame
    ), "Result should be a single pandas DataFrame"
    assert df_accel.shape == (46, 3)
    df_time = tsdf.load_dataframe_from_binaries(
        [metadata["time_t1.bin"], metadata["time_t2.bin"]], ConcatenationType.rows
    )

    assert isinstance(
        df_time, pd.DataFrame
    ), "Result should be a single pandas DataFrame"
    assert df_time.shape == (46, 1)


def test_load_dataframe_concatenation_columns(shared_datadir):
    metadata = tsdf.load_metadata_from_path(
        shared_datadir / "hierarchical/hierarchical_meta.json"
    )
    df_t1 = tsdf.load_dataframe_from_binaries(
        [metadata["time_t1.bin"], metadata["accelerometer_t1.bin"]],
        ConcatenationType.columns,
    )

    assert isinstance(df_t1, pd.DataFrame), "Result should be a single pandas DataFrame"
    assert df_t1.shape == (17, 4)
    df_t2 = tsdf.load_dataframe_from_binaries(
        [metadata["time_t2.bin"], metadata["accelerometer_t2.bin"]],
        ConcatenationType.columns,
    )

    assert isinstance(df_t2, pd.DataFrame), "Result should be a single pandas DataFrame"
    assert df_t2.shape == (29, 4)


def test_load_dataframe_concatenation_none(shared_datadir):
    metadata = tsdf.load_metadata_from_path(
        shared_datadir / "hierarchical/hierarchical_meta.json"
    )
    dataframes = tsdf.load_dataframe_from_binaries(
        [
            metadata["time_t1.bin"],
            metadata["accelerometer_t1.bin"],
            metadata["accelerometer_t2.bin"],
        ],
        ConcatenationType.none,
    )
    assert len(dataframes) == 3
    assert dataframes[0].shape == (17, 1)
    assert dataframes[1].shape == (17, 3)
    assert dataframes[2].shape == (29, 3)

