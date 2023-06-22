import os
import json
import glob
from tsdf.constants import METADATA_NAMING_PATTERN
from tsdf.io import get_files_matching, load_metadata_file, load_metadatas_from_dir
from typing import AnyStr, Dict, Any

# the old (TSDB) and new field (TSDF) names
TSDB_TSDF_KEY_MAP = {
    "project_id": "study_id",
    "quantities": "channels",
    "datatype": "data_type",
    "start_datetime_iso8601": "start_iso8601",
    "end_datetime_iso8601": "end_iso8601",
}

# the field whose value should be an array
TSDB_ARRAY_KEYS = {"channels", "units"}


def _rename_keys_in_metadata(old_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    This function renames the keys in a metadata file.
    If a key in the metadata matches a key in the provided dictionary, it is renamed to the corresponding value in the dictionary.
    It handles nested dictionaries and lists of dictionaries.

    :param old_dict: The metadata file (dictionary) with keys to rename
    :return: The updated metadata file (dictionary)
    """
    new_dict = {}
    for key, value in old_dict.items():
        new_key = TSDB_TSDF_KEY_MAP.get(key, key)
        if isinstance(value, dict):
            new_dict[new_key] = _rename_keys_in_metadata(value)
        elif isinstance(value, list):
            new_dict[new_key] = [
                _rename_keys_in_metadata(v) if isinstance(v, dict) else v for v in value
            ]
        else:
            new_dict[new_key] = value
    return new_dict


def _convert_to_array(data: Dict[str, Any], key: str) -> Dict[str, Any]:
    """
    This function converts the value of a specified key in a dictionary to an array if it's not already an array.
    It handles nested dictionaries and lists of dictionaries.

    :param data: The dictionary with a value to convert
    :param key: The key in the dictionary whose value to convert
    :return: The updated dictionary
    """
    for k, value in data.items():
        if k == key and not isinstance(value, list):
            data[k] = [str(value)]
        elif isinstance(value, dict):
            data[k] = _convert_to_array(value, key)
        elif isinstance(value, list):
            data[k] = [
                _convert_to_array(v, key) if isinstance(v, dict) else v for v in value
            ]
    return data


def _transform_tsdb_to_tsdf(filepath: str) -> None:
    """
    This function reads a JSON file, renames keys and converts a value in the loaded dictionary, then saves it back to the file.

    :param filepath: The path to the JSON file to process
    """
    with open(filepath, "r") as f:
        data = json.load(f)
    # rename the keys in the dictionary
    data = _rename_keys_in_metadata(data)
    # convert the values of the specified keys to arrays
    for key in TSDB_ARRAY_KEYS:
        data = _convert_to_array(data, key)
    with open(filepath, "w") as f:
        json.dump(data, f)


def update_metadatas_tsdb_to_tsdf(directory: str) -> None:
    """
    This function converts all metadata files in a directory (and its subdirectories) from TSDB (legacy) to TSDF (0.1) format.
    It walks through all files in a directory (and its subdirectories),
    and processes all files with a .json extension.

    :param directory: The directory to process files in
    """
    for filepath in get_files_matching(directory, METADATA_NAMING_PATTERN):
        _transform_tsdb_to_tsdf(filepath)


# Path to the directory containing the metadata files
DIR = "/Users/vedran/Desktop/1_patient_week"

# Convert all metadata files in the directory from TSDB to TSDF format
# update_metadatas_tsdb_to_tsdf(DIR)

load_metadatas_from_dir(DIR)
