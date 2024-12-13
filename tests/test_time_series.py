import numpy as np
import pandas as pd

import tsdf
from tsdf.time_series import TSDFTimeSeries, ChannelMetadata, channel_group_name, read_single_time_series_metadata, read_multi_time_series_metadata, read_dataframe, write_dataframe, get_metadata
from tsdf.constants import ConcatenationType

def test_channel_group_name():
    assert channel_group_name("file.bin") == None
    assert channel_group_name("no_extension") == None
    assert channel_group_name("file.suffix.bin") == "suffix"
    assert channel_group_name("dir/my-file-suffix.bin") == "suffix"
    assert channel_group_name("dir/my_file_suffix.bin") == "suffix"

def test_read_single_time_series(shared_datadir):
    """
    Test reading of a metadata file with a single time_series split over multiple data files
    """
    file = shared_datadir / "ppp_format_meta.json"
    time_series = read_single_time_series_metadata(file)
    assert isinstance(time_series, TSDFTimeSeries)
    assert time_series.channels == ["time", "acceleration_x", "acceleration_y", "acceleration_z", "rotation_x", "rotation_y", "rotation_z"]
    assert [g.name for g in time_series.channel_groups] == ["time", "samples"]
    # compare time_series's read to old style interface
    metas = tsdf.load_metadata_from_path(file)
    time_data = time_series.read_numpy(["time"])
    time_data2 = tsdf.load_ndarray_from_binary(metas["ppp_format_time.bin"])
    assert np.array_equal(time_data, time_data2)
    imu_data = time_series.read_numpy(["acceleration_x", "acceleration_y", "acceleration_z", "rotation_x", "rotation_y", "rotation_z"])
    imu_data2 = tsdf.load_ndarray_from_binary(metas["ppp_format_samples.bin"])
    assert np.array_equal(imu_data, imu_data2)
    # compare reading dataframes
    df = time_series.read_dataframe()
    df2 = tsdf.load_dataframe_from_binaries(list(metas.values()), concatenation=ConcatenationType.columns)
    pd.testing.assert_frame_equal(df, df2)
    assert get_metadata(df) == time_series.meta, "df should have metadata"
    # reading only some columns
    time_df = time_series.read_dataframe(["time"])
    assert np.array_equal(time_df.to_numpy(), time_data[:,None])
    acc_df = time_series.read_dataframe(["acceleration_x", "acceleration_y", "acceleration_z"])
    assert np.array_equal(acc_df.to_numpy(), imu_data[:,0:3])

def test_read_multi_time_series(shared_datadir):
    file = shared_datadir / "hierarchical_meta.json"
    time_series = read_multi_time_series_metadata(file)
    assert len(time_series) == 4

def test_write_time_series(shared_datadir):
    file = shared_datadir / "ppp_format_meta.json"
    file2 = shared_datadir / "tmp_test_write_time_series.json"
    df = read_dataframe(file)
    write_dataframe(file2, df)
    df2 = read_dataframe(file2)
    pd.testing.assert_frame_equal(df, df2)
    assert get_metadata(df).to_dict() == get_metadata(df2).to_dict()

def test_write_time_series_subset(shared_datadir):
    """
    Test writing and reading a subset of the channels
    """
    file = shared_datadir / "ppp_format_meta.json"
    file2 = shared_datadir / "test_write_time_series_subset.json"
    df = read_dataframe(file, ["time", "acceleration_x"])
    write_dataframe(file2, df)
    df2 = read_dataframe(file2)
    pd.testing.assert_frame_equal(df, df2)
    assert get_metadata(df).to_dict() == get_metadata(df2).to_dict()

def test_write_time_series_add_channel(shared_datadir):
    file = shared_datadir / "ppp_format_meta.json"
    file2 = shared_datadir / "test_write_time_series_add_channel.json"
    df = read_dataframe(file, ["time"])
    df['double_time'] = 2 * df['time']
    df.tsdf_metadata.add_channel('double_time', ChannelMetadata('m/s/s'))
    write_dataframe(file2, df)
    df2 = read_dataframe(file2)
    pd.testing.assert_frame_equal(df, df2)
    assert get_metadata(df).to_dict() == get_metadata(df2).to_dict()
