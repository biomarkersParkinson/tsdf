import numpy as np
import pandas as pd
from tsdf import read_tsdf, write_binary, TSDFMetadata

def test_write_binary(shared_datadir):
    """Test writing of binary files from loaded data (e.g., NumPy array)."""
    """Save a NumPy array as a binary file."""
    
    test_meta_file_name = "flat_meta.json"
    test_file_name = "tmp_test_output_1.bin"
    
    rs = np.random.RandomState(seed=42)
    data_original = rs.rand(17, 1).astype(np.float32)
    with open(shared_datadir / test_meta_file_name, "r") as file:
        metadatas = read_tsdf.load_metadata_file(file)
        write_binary.write_binary_file(
            shared_datadir,
            test_file_name,
            data_original,
            metadatas["audio_voice_089.raw"].get_plain_tsdf_dict_copy(),
        )

    # Read file again to check contents
    path = shared_datadir / test_file_name
    with open(path, "rb") as fid:
        data_written = np.fromfile(fid, dtype="<f4")
        data_written = data_written.reshape(17, 1)
        assert(np.array_equal(data_original, data_written))


def test_write_dataframe(shared_datadir):
    """Test writing of binary files from a loaded data frame."""
    test_file_name = "tmp_test_pandas.bin"
    test_meta_dict = {
        "study_id": "voicedata",
        "subject_id": "recruit089",
        "device_id": "audiotechnica02",
        "endianness": "little",
        "metadata_version": "0.1",
        "start_iso8601": "2016-08-09T10:31:00.000+00:00",
        "end_iso8601": "2016-08-10T10:31:30.000+00:00",
        "sampling_rate": 44100,
        "rows": 17,
        "channels": [
            "left",
            "right",
            "middle"
        ],
        "units": [
            "unitless",
            "unitless",
            "unitless",
        ],
        "compression": "none",
        "data_type": "int",
        "bits": 16,
        "file_name": test_file_name
    }
    test_meta = TSDFMetadata(test_meta_dict, shared_datadir)
    
    rs = np.random.RandomState(seed=42)
    data_original = rs.rand(17, 3).astype(np.int16)
    df = pd.DataFrame(data_original, columns=test_meta.channels)
    print(df.shape)
    write_binary.write_dataframe_to_binaries(shared_datadir, df, [test_meta])

    # Read file again to check contents
    path = shared_datadir / test_file_name
    with open(path, "rb") as fid:
        data_written = np.fromfile(fid, dtype="<i2")
        data_written = data_written.reshape(17, 3)
        assert(np.array_equal(data_original, data_written))

    #TODO: don't provide all data props (type, etc), also channels, in metadata, but infer from data and test that it is correct
