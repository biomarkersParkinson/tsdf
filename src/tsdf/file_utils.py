import json
import os
import glob
from typing import Dict, Any


def get_files_matching(directory: str,  criteria: str) -> list:
    """
    Get all files matching the criteria in the directory and its subdirectories.

    :param directory: directory to search in.
    :param criteria: criteria to match (e.g., `**meta.json`).

    :return: list of files matching the criteria.
    """
    return glob.glob(os.path.join(directory, criteria), recursive=True)


def write_to_file(dict: Dict[str, Any], dir_path: str, file_name: str) -> None:
    """
    Write a dictionary to a json file.

    :param dict: Dictionary to be written.
    :param dir_path: Path to the directory where the file will be saved.
    :param file_name: Name of the file to be saved.
    """
    path = os.path.join(dir_path, file_name)
    with open(path, "w") as convert_file:
        convert_file.write(json.dumps(dict, indent=4))

