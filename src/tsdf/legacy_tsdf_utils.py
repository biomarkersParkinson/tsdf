import json
from typing import Dict, Any
from tsdf.constants import METADATA_NAMING_PATTERN
from tsdf import file_utils 


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

def convert_tsdb_to_tsdf(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converts a data from TSDB (legacy) to TSDF (0.1) format.

    :param data: The data in legacy (tsdb) format.
    :return: The data in tsdf format.
    """
     # rename the keys in the dictionary
    new_data = _rename_keys_in_metadata(data)
    # convert the values of the specified keys to arrays
    for key in TSDB_ARRAY_KEYS:
        new_data = _convert_to_array(new_data, key)

    return new_data


def generate_tsdf_metadata_from_tsdb(filepath_existing: str, filepath_new: str) -> None:
    """
    This function creates a metadata file (JSON) file in TSDF (0.1) format from a TSDB (legacy) file.

    :param filepath_existing: The path to the JSON file to process
    :param filepath_new: The path to the new JSON file
    """
    with open(filepath_existing, "r") as f:
        data = json.load(f)
    new_data = convert_tsdb_to_tsdf(data)
    with open(filepath_new, "w") as f:
        json.dump(new_data, f)

def convert_file_tsdb_to_tsdf(filepath: str) -> None:
    """
    This function converts a metadata file (JSON) from TSDB (legacy) to TSDF (0.1) format. It overwrites the original file.

    :param filepath: The path to the JSON file to process
    """
    with open(filepath, "r") as f:
        data = json.load(f)
        new_data = convert_tsdb_to_tsdf(data)
    with open(filepath, "w") as f:
        json.dump(new_data, f)


def convert_files_tsdb_to_tsdf(directory: str) -> None:
    """
    This function converts all metadata files in a directory (and its subdirectories) from TSDB (legacy) to TSDF (0.1) format.
    It walks through all files in a directory (and its subdirectories),
    and processes all files with a .json extension.

    :param directory: The directory to process files in
    """
    
    for filepath in file_utils.get_files_matching(directory, METADATA_NAMING_PATTERN):
        convert_file_tsdb_to_tsdf(filepath)
