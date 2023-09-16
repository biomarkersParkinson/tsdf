import os

# Reference: https://arxiv.org/abs/2211.11294

SUPPORTED_TSDF_VERSIONS = ["0.1"]
""" List of currently supported versions. """

MANDATORY_TSDF_KEYS = {
    "0.1": [
        "subject_id",
        "study_id",
        "device_id",
        "endianness",
        "metadata_version",
        "data_type",
        "bits",
        "rows",
        "channels",
        "units",
        "file_name",
        "start_iso8601",
        "end_iso8601",
    ]
}
""" Dictionary linking mandatory keys for different versions """

MANDATORY_TSDF_KEYS_VALUES = {
    "0.1": [
        "str",
        "str",
        "str",
        "str",
        "str",
        "str",
        "int",
        "int",
        "list",
        "list",
        "str",
        "str",
        "str",
    ]
}
""" Dictionary linking mandatory keys to their values"""

KEY_VALUE_TYPES = {
    "int": int,
    "list": list,
    "float": float,
    "str": str
    # etc
}
""" List of data types that are supported within the TSDF metadata file. """

METADATA_NAMING_PATTERN = "**meta.json"
""" Naming convention for the metadata files. ** allows for any prefix, including additional directories. """


class TestConstants:
    """Class containing constants used for testing and demonstration."""

    TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "tests", "data")

    """ Path to the test data directory. """
    TEST_OUTPUT_DATA_DIR = os.path.join(TEST_DATA_DIR, "outputs")
    """ Path to the test output data directory. """

    TEST_DATA_FILES = {
        "flat": os.path.join(TEST_DATA_DIR, "flat_meta.json"),
        "hierarchical": os.path.join(TEST_DATA_DIR, "hierarchical_meta.json"),
        "wrongversion": os.path.join(TEST_DATA_DIR, "wrongversion_meta_fail.json"),
        "missingkey": os.path.join(TEST_DATA_DIR, "missingkey_meta_fail.json"),
        "example_10_3_int16": os.path.join(TEST_DATA_DIR, "example_10_3_int16_meta.json"),
        "ppp": os.path.join(TEST_DATA_DIR, "ppp_format_meta.json"),
        "legacy": os.path.join(TEST_DATA_DIR, "ppp_format_meta_legacy.json"),
    }
    """ Dictionary used for accessing test data files. """

    METADATA_EXTENSION = "_meta.json"
    """ Suffix and extension used to denote metadata files. """

    BINARY_EXTENSION = ".bin"
