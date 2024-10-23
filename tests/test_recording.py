import numpy as np
import pandas as pd

import tsdf
from tsdf.recording import TSDFRecording, channel_group_name, read_single_recording_metadata, read_multi_recording_metadata, read_dataframe, write_dataframe, get_metadata
from tsdf.constants import ConcatenationType

def test_channel_group_name():
    assert channel_group_name("file.bin") == None
    assert channel_group_name("no_extension") == None
    assert channel_group_name("file.suffix.bin") == "suffix"
    assert channel_group_name("dir/my-file-suffix.bin") == "suffix"
    assert channel_group_name("dir/my_file_suffix.bin") == "suffix"

def test_read_single_recording(shared_datadir):
    """
    Test reading of a metadata file with a single recording split over multiple data files
    """
    file = shared_datadir / "ppp_format_meta.json"
    recording = read_single_recording_metadata(file)
    assert isinstance(recording, TSDFRecording)
    assert recording.channels == ["time", "acceleration_x", "acceleration_y", "acceleration_z", "rotation_x", "rotation_y", "rotation_z"]
    assert [g.name for g in recording.channel_groups] == ["time", "samples"]
    # compare recording's read to old style interface
    metas = tsdf.load_metadata_from_path(file)
    time_data = recording.read_numpy(["time"])
    time_data2 = tsdf.load_ndarray_from_binary(metas["ppp_format_time.bin"])
    assert np.array_equal(time_data, time_data2)
    imu_data = recording.read_numpy(["acceleration_x", "acceleration_y", "acceleration_z", "rotation_x", "rotation_y", "rotation_z"])
    imu_data2 = tsdf.load_ndarray_from_binary(metas["ppp_format_samples.bin"])
    assert np.array_equal(imu_data, imu_data2)
    # compare reading dataframes
    df = recording.read_dataframe()
    df2 = tsdf.load_dataframe_from_binaries(list(metas.values()), concatenation=ConcatenationType.columns)
    pd.testing.assert_frame_equal(df, df2)
    assert get_metadata(df) == recording.meta, "df should have metadata"
    # reading only some columns
    time_df = recording.read_dataframe(["time"])
    assert np.array_equal(time_df.to_numpy(), time_data[:,None])
    acc_df = recording.read_dataframe(["acceleration_x", "acceleration_y", "acceleration_z"])
    assert np.array_equal(acc_df.to_numpy(), imu_data[:,0:3])

def test_read_multi_recording(shared_datadir):
    file = shared_datadir / "hierarchical_meta.json"
    recordings = read_multi_recording_metadata(file)
    assert len(recordings) == 4

def test_write_recording(shared_datadir):
    file = shared_datadir / "ppp_format_meta.json"
    file2 = shared_datadir / "tmp_test_write_recording.json"
    df = read_dataframe(file)
    write_dataframe(file2, df)
    df2 = read_dataframe(file2)
    pd.testing.assert_frame_equal(df, df2)
    assert get_metadata(df).to_dict() == get_metadata(df2).to_dict()
