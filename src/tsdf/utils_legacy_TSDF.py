import os
import json
import glob
from tsdf.io import load_metadata_file
from typing import Dict, Any

# the old (TSDB) and new field (TSDF) names
tsdb_tsdf_key_map = {
    "project_id": "study_id",
    "quantities": "channels",
    "datatype": "data_type",
    "start_datetime_iso8601": "start_iso8601",
    "end_datetime_iso8601": "end_iso8601",
}

# the field whose value should be an array
tsdb_array_keys = {"channels", "units"}


def transform_legacy_to_tsdf(file):
    """Convert a legacy TSDF file to a TSDF file"""
    # Load the legacy metadata file (json file)
    data = json.load(file)

    # Convert the legacy metadata to a TSDF metadata


def rename_keys_in_metadata(old_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    This function renames the keys in a metadata file.
    If a key in the metadata matches a key in the provided dictionary, it is renamed to the corresponding value in the dictionary.
    It handles nested dictionaries and lists of dictionaries.

    :param old_dict: The metadata file (dictionary) with keys to rename
    :return: The updated metadata file (dictionary)
    """
    new_dict = {}
    for key, value in old_dict.items():
        new_key = tsdb_tsdf_key_map.get(key, key)
        if isinstance(value, dict):
            new_dict[new_key] = rename_keys_in_metadata(value)
        elif isinstance(value, list):
            new_dict[new_key] = [
                rename_keys_in_metadata(v) if isinstance(v, dict) else v for v in value
            ]
        else:
            new_dict[new_key] = value
    return new_dict


def convert_to_array(data: Dict[str, Any], key: str) -> Dict[str, Any]:
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
            data[k] = convert_to_array(value, key)
        elif isinstance(value, list):
            data[k] = [
                convert_to_array(v, key) if isinstance(v, dict) else v for v in value
            ]
    return data


def process_file(filepath: str) -> None:
    """
    This function reads a JSON file, renames keys and converts a value in the loaded dictionary, then saves it back to the file.

    :param filepath: The path to the JSON file to process
    """
    with open(filepath, "r") as f:
        data = json.load(f)
    # rename the keys in the dictionary
    data = rename_keys_in_metadata(data)
    # convert the values of the specified keys to arrays
    for key in tsdb_array_keys:
        data = convert_to_array(data, key)
    with open(filepath, "w") as f:
        json.dump(data, f)


def update_metadatas_TSDB_to_TSDF(directory: str) -> None:
    """
    This function converts all metadata files in a directory (and its subdirectories) from TSDB (legacy) to TSDF (0.1) format.
    It walks through all files in a directory (and its subdirectories),
    and processes all files with a .json extension.

    :param directory: The directory to process files in
    """
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".json"):
                filepath = os.path.join(dirpath, filename)
                process_file(filepath)
