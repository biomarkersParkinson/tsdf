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
