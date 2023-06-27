import os

TESTDATA_DIR = os.path.join(os.path.dirname(__file__), "data")
""" Path to the test data directory. """
TEST_OUTPUT_DATA_DIR = os.path.join(TESTDATA_DIR, "outputs")
""" Path to the test output data directory. """

TESTDATA_FILES = {
    "flat": os.path.join(TESTDATA_DIR, "flat_meta.json"),
    "hierarchical": os.path.join(TESTDATA_DIR, "hierarchical_meta.json"),
    "wrongversion": os.path.join(TESTDATA_DIR, "wrongversion_meta_fail.json"),
    "missingkey": os.path.join(TESTDATA_DIR, "missingkey_meta_fail.json"),
    "dummy_10_3_int16": os.path.join(TESTDATA_DIR, "dummy_10_3_int16_meta.json"),
    "ppp": os.path.join(TESTDATA_DIR, "ppp_format_meta.json"),
}
""" Dictionary used for accessing test data files. """

METADATA_EXTENSION = "_meta.json"
""" Suffix and extension used to denote metadata files. """

BINARY_EXTENSION = ".bin"
""" Suffix and extension used to denote binary files. """
