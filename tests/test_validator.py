from tsdf import validator

def test_validate_valid_file(shared_datadir):
    is_valid = validator.validate_tsdf_format(shared_datadir / "ppp_format_meta.json")
    assert(is_valid)

def test_validate_invalid_file(shared_datadir):
    is_valid = validator.validate_tsdf_format(shared_datadir / "missingkey_meta_fail.json")
    assert(not is_valid)
