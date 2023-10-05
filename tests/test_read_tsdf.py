import tsdf 


def test_load_metadata_file(shared_datadir):
    """Test that a json file gets loaded correctly."""
    with open(shared_datadir / "hierarchical_meta.json", "r") as file:
        data = tsdf.load_metadata_file(file)
        assert(len(data) == 4)

def test_load_metadata_legacy_file(shared_datadir):
    """Test that a json file gets loaded correctly."""
    with open(shared_datadir / "ppp_format_meta_legacy.json", "r") as file:
        data = tsdf.load_metadata_legacy_file(file)
        assert(len(data) == 2)

def test_load_metadata_from_path(shared_datadir):
    """Test that a json file from a path gets loaded correctly."""
    data = tsdf.load_metadata_from_path(shared_datadir / "hierarchical_meta.json")
    assert(len(data) == 4)

def test_load_metadata_string(shared_datadir):
    """Test that a json object gets loaded from a string correctly."""
    with open(shared_datadir / "hierarchical_meta.json", "r") as file:
        json_string = file.read()
        data = tsdf.load_metadata_string(json_string)
        assert(len(data) == 4)

def test_load_metadatas_from_dir(shared_datadir):
    """Test that all metadata files gets loaded from a directory correctly."""
    data = tsdf.load_metadatas_from_dir(shared_datadir)
    assert(len(data) == 6)
