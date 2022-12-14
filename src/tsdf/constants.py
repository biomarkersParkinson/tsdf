# Reference: https://arxiv.org/abs/2211.11294

# List of currently supported versions
SUPPORTED_VERSIONS = ["0.1"]

# Dictionary linking mandatory keys for different versions
MANDATORY_KEYS = { "0.1" : ["subject_id","study_id","device_id", "endianness",
                            "metadata_version","data_type", "bits", "rows",
                            "channels", "units","file_name","start_iso8601","end_iso8601"] }

# Dictionary linking mandatory keys to their values
MANDATORY_KEYS_VALUES = { "0.1" : ["str","str","str","str",
                                    "str","str","int","int",
                                    "list","list","str","str","str"] }

# TODO: add description
KNOWN_TYPES = {
    'int': int,
    'list': list,
    'float': float,
    'str': str
    # etc
}