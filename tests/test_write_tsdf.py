import numpy as np
import tsdf
from tsdf import TSDFMetadata
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

    assert(len(meta) == 3)
    assert(meta[test_name + "_1.bin"].rows == 17)
    assert(meta[test_name + "_2.bin"].rows == 15)
    assert(meta[test_name + "_3.bin"].rows == 10)

def test_bin_processing_and_writing_metadata(shared_datadir):
    """Test binary file reading, processing, and writing of the new binary and metadata files."""
    # Load existing TSDF metadata and the corresponding binary data
    name = "example_10_3_int16"
    metas = tsdf.load_metadata_from_path(shared_datadir / (name + "_meta.json"))
    original_metadata = metas[name + ".bin"]
    original_data = tsdf.load_binary_from_metadata(original_metadata)

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
    assert(final_data.shape == (10, 3))
    assert(final_data.dtype == "float32")
