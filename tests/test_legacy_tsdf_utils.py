import tsdf
from tsdf import legacy_tsdf_utils


def test_conversion(shared_datadir):
    """Test whether the conversion from TSDB (legacy metadata format) to TSDF works. """

    path_to_file = shared_datadir / "ppp_format_meta_legacy.json"
    path_to_new_file = shared_datadir / "tmp_test_ppp_format_meta.json"
    path_to_existing_tsdf_file = shared_datadir / "ppp_format_meta.json"

    # Generate a TSDF metadata file from TSDB
    legacy_tsdf_utils.generate_tsdf_metadata_from_tsdb(path_to_file, path_to_new_file)

    # Load the generated metadata file
    new_meta = tsdf.load_metadata_from_path(path_to_new_file)

    # Load the existing metadata file
    existing_meta = tsdf.load_metadata_from_path(path_to_existing_tsdf_file)

    # Compare the two metadata files (whether the mapped TSDFs fields are the same)
    assert(new_meta["ppp_format_time.bin"].get_plain_tsdf_dict_copy() ==
        existing_meta["ppp_format_time.bin"].get_plain_tsdf_dict_copy())

    assert(new_meta["ppp_format_samples.bin"].get_plain_tsdf_dict_copy() ==
        existing_meta["ppp_format_samples.bin"].get_plain_tsdf_dict_copy())
