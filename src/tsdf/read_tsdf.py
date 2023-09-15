"""
Module for reading TSDF files.

Reference: https://arxiv.org/abs/2211.11294
"""

import json
import os
from typing import Dict, List
from tsdf import file_utils 
from tsdf.constants import METADATA_NAMING_PATTERN
from tsdf import parse_metadata 
from tsdf import legacy_tsdf_utils 
from tsdf.tsdfmetadata import TSDFMetadata


def load_metadata_file(file) -> Dict[str, TSDFMetadata]:
    """Loads a TSDF metadata file, returns a dictionary

    :param file: file object containing the TSDF metadata.

    :return: dictionary of TSDFMetadata objects.
    """

    # The data is isomorphic to a JSON
    data = json.load(file)

    abs_path = os.path.realpath(file.name)

    # Parse the data and verify that it complies with TSDF requirements
    return parse_metadata.read_data(data, abs_path)

def load_metadata_legacy_file(file) -> Dict[str, TSDFMetadata]:
    """Loads a TSDB metadata file, i.e., legacy format of the TSDF. It returns a dictionary representing the metadata.

    :param file: file object containing the TSDF metadata.

    :return: dictionary of TSDFMetadata objects.
    """

    # The data is isomorphic to a JSON
    legacy_data = json.load(file)

    abs_path = os.path.realpath(file.name)

    tsdf_data = legacy_tsdf_utils.convert_tsdb_to_tsdf(legacy_data)

    # Parse the data and verify that it complies with TSDF requirements
    return parse_metadata.read_data(tsdf_data, abs_path)

def load_metadatas_from_dir(
    dir_path: str, naming_pattern=METADATA_NAMING_PATTERN
) -> List[Dict[str, TSDFMetadata]]:
    """
    Loads all TSDF metadata files in a directory, returns a dictionary

    :param dir_path: path to the directory containing the TSDF metadata files.
    :param naming_pattern: (optional) naming pattern of the TSDF metadata files .

    :return: dictionary of TSDFMetadata objects.
    """
    # Get all files in the directory
    file_paths = file_utils.get_files_matching(dir_path, naming_pattern)

    # Load all files
    metadatas = []
    for file_path in file_paths:
        metadata = load_metadata_from_path(file_path)
        metadatas.append(metadata)

    return metadatas


def load_metadata_from_path(path: str) -> Dict[str, TSDFMetadata]:
    """
    Loads a TSDF metadata file, returns a dictionary

    :param path: path to the TSDF metadata file.

    :return: dictionary of TSDFMetadata objects.
    """
    # The data is isomorphic to a JSON
    with open(path, "r") as file:
        data = json.load(file)

    abs_path = os.path.realpath(path)
    # Parse the data and verify that it complies with TSDF requirements
    return parse_metadata.read_data(data, abs_path)


def load_metadata_string(json_str) -> Dict[str, TSDFMetadata]:
    """
    Loads a TSDF metadata string, returns a dictionary.

    :param json_str: string containing the TSDF metadata.

    :return: dictionary of TSDFMetadata objects.
    """

    # The data is isomorphic to a JSON
    data = json.loads(json_str)

    # Parse the data and verify that it complies with TSDF requirements
    return parse_metadata.read_data(data, "")
