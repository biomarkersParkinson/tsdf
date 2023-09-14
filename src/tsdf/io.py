"""
Module for reading and writing TSDF files.

Reference: https://arxiv.org/abs/2211.11294
"""

import glob
import json
import os
from typing import Any, Dict, List
import numpy as np
from tsdf import io_metadata
from tsdf.constants import METADATA_NAMING_PATTERN
from tsdf.numpy_utils import (
    data_type_numpy_to_tsdf,
    data_type_tsdf_to_numpy,
    bits_numpy_to_tsdf,
    bytes_tsdf_to_numpy,
    endianness_numpy_to_tsdf,
    endianness_tsdf_to_numpy,
    rows_numpy_to_tsdf,
)
from tsdf.tsdf_metadata import TSDFMetadata, TSDFMetadataFieldValueError


def load_metadata_file(file) -> Dict[str, TSDFMetadata]:
    """Loads a TSDF metadata file, returns a dictionary

    :param file: file object containing the TSDF metadata.

    :return: dictionary of TSDFMetadata objects.
    """

    # The data is isomorphic to a JSON
    data = json.load(file)

    abs_path = os.path.realpath(file.name)

    # Parse the data and verify that it complies with TSDF requirements
    return io_metadata.read_data(data, abs_path)

def load_metadata_legacy_file(file) -> Dict[str, TSDFMetadata]:
    """Loads a TSDB metadata file, i.e., legacy format of the TSDF. It returns a dictionary representing the metadata.

    :param file: file object containing the TSDF metadata.

    :return: dictionary of TSDFMetadata objects.
    """
    from tsdf.utils_legacy_tsdf import convert_tsdb_to_tsdf

    # The data is isomorphic to a JSON
    legacy_data = json.load(file)

    abs_path = os.path.realpath(file.name)

    tsdf_data = convert_tsdb_to_tsdf(legacy_data)

    # Parse the data and verify that it complies with TSDF requirements
    return io_metadata.read_data(tsdf_data, abs_path)


def get_files_matching(directory: str,  criteria: str) -> list:
    """
    Get all files matching the criteria in the directory and its subdirectories.

    :param directory: directory to search in.
    :param criteria: criteria to match (e.g., `**meta.json`).

    :return: list of files matching the criteria.
    """
    return glob.glob(os.path.join(directory, criteria), recursive=True)


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
    file_paths = get_files_matching(dir_path, naming_pattern)

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
    return io_metadata.read_data(data, abs_path)


def load_metadata_string(json_str) -> Dict[str, TSDFMetadata]:
    """
    Loads a TSDF metadata string, returns a dictionary.

    :param json_str: string containing the TSDF metadata.

    :return: dictionary of TSDFMetadata objects.
    """

    # The data is isomorphic to a JSON
    data = json.loads(json_str)

    # Parse the data and verify that it complies with TSDF requirements
    return io_metadata.read_data(data, "")


def load_binary_from_metadata(
    metadata_dir: str, metadata: TSDFMetadata, start_row: int = 0, end_row: int = -1
) -> np.ndarray:
    """
    Use metadata properties to load and return numpy array from a binary file.

    :param metadata_dir: path to the directory containing the TSDF metadata files.
    :param metadata: TSDFMetadata object.
    :param start_row: (optional) first row to load.
    :param end_row: (optional) last row to load. If -1, load all rows.

    :return: numpy array containing the data."""
    bin_path = os.path.join(metadata_dir, metadata.file_name)
    return load_binary_file(
        bin_path,
        metadata.data_type,
        metadata.bits,
        metadata.endianness,
        metadata.rows,
        len(metadata.channels),
        start_row,
        end_row,
    )


def load_binary_file(
    bin_file_path: str,
    data_type: str,
    n_bits: int,
    endianness: str,
    n_rows: int,
    n_columns: int,
    start_row: int = 0,
    end_row: int = -1,
) -> np.ndarray:
    """
    Use provided parameters to load and return a numpy array from a binary file

    :param bin_file_path: path to the binary file.
    :param data_type: data type of the binary file.
    :param n_bits: number of bits per value.
    :param endianness: endianness of the binary file.
    :param n_rows: number of rows in the binary file.
    :param n_columns: number of columns in the binary file.
    :param start_row: (optional) first row to load.
    :param end_row: (optional) last row to load. If -1, load all rows.

    :return: numpy array containing the data.
    """

    s_endianness = endianness_tsdf_to_numpy(endianness)
    s_type = data_type_tsdf_to_numpy(data_type)
    s_n_bytes = bytes_tsdf_to_numpy(n_bits)
    format_string = "".join([s_endianness, s_type, s_n_bytes])

    # Load the data and reshape
    with open(bin_file_path, "rb") as fid:
        fid.seek(start_row * n_columns * n_bits // 8)
        if end_row == -1:
            end_row = n_rows
        buffer = fid.read((end_row - start_row) * n_columns * n_bits // 8)
        values = np.frombuffer(buffer, dtype=format_string)
        if n_columns > 1:
            values = values.reshape((-1, n_columns))

    # Check whether the number of rows matches the metadata
    if values.shape[0] != end_row - start_row:
        raise Exception("Number of rows doesn't match file length.")

    return values


def get_metadata_from_ndarray(data: np.ndarray) -> Dict[str, Any]:
    """
    Retrieve metadata information encoded in the NumPy array.

    :param data: NumPy array containing the data.

    :return: dictionary containing the metadata.
    """

    metadata = {
        "data_type": data_type_numpy_to_tsdf(data),
        "bits": bits_numpy_to_tsdf(data),
        "endianness": endianness_numpy_to_tsdf(data),
        "rows": rows_numpy_to_tsdf(data),
    }
    return metadata


def write_binary_file(
    file_dir: str, file_name: str, data: np.ndarray, metadata: dict
) -> TSDFMetadata:
    """
    Save binary file based on the provided NumPy array.

    :param file_dir: path to the directory where the file will be saved.
    :param file_name: name of the file to be saved.
    :param data: NumPy array containing the data.
    :param metadata: dictionary containing the metadata.

    :return: TSDFMetadata object.
    """
    path = os.path.join(file_dir, file_name)
    data.tofile(path)
    metadata.update(get_metadata_from_ndarray(data))
    metadata.update({"file_name": file_name})

    return TSDFMetadata(metadata, file_dir)


def write_metadata(metadatas: List[TSDFMetadata], file_name: str) -> None:
    """
    Combine and save the TSDF metadata objects as a json file.

    :param metadatas: List of TSDFMetadata objects to be saved.
    :param file_name: Name of the file to be saved. The file will be saved in the directory of the first TSDFMetadata object in the list.

    :raises TSDFMetadataFieldValueError: if the metadata files cannot be combined (e.g. they have no common fields) or if the list of TSDFMetadata objects is empty.
    """
    if len(metadatas) == 0:
        raise TSDFMetadataFieldValueError(
            "Metadata cannot be saved, as the list of TSDFMetadata objects is empty."
        )

    if len(metadatas) == 1:
        meta = metadatas[0]
        write_to_file(meta.get_plain_tsdf_dict_copy(), meta.file_dir_path, file_name)
        return

    # Ensure that the metadata files can be combined
    io_metadata.confirm_dir_of_metadata(metadatas)

    plain_meta = [meta.get_plain_tsdf_dict_copy() for meta in metadatas]
    overlap = extract_common_fields(plain_meta)
    if not overlap:
        raise TSDFMetadataFieldValueError(
            "Metadata files mist have at least one common field. Otherwise, they should be stored separately."
        )

    if len(plain_meta) > 0:
        overlap["sensors"] = calculate_ovelaps_rec(plain_meta)
    write_to_file(overlap, metadatas[0].file_dir_path, file_name)


def extract_common_fields(metadatas: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Extract the fields that are the same for all the metadata files.
    A new dict is created and the fields are removed from the original dictionaries.

    :param metadatas: List of dictionaries containing the metadata.

    :return: Dictionary containing the common fields.
    """
    meta_overlap: dict = {}

    # Return empty dict if metadatas is empty
    if len(metadatas) == 0:
        return meta_overlap
    if len(metadatas) == 1:
        return metadatas.pop(0)
    init_metadata = metadatas[0]
    for key, value in init_metadata.items():
        key_in_all = True
        for curr_meta in metadatas[1:]:
            if key not in curr_meta.keys() or curr_meta[key] != value:
                key_in_all = False
        if key_in_all:
            meta_overlap[key] = value
    for key, _ in meta_overlap.items():
        for meta_dict in metadatas:
            meta_dict.pop(key)
    return meta_overlap


def calculate_ovelaps_rec(metadatas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    A recursive call that optimises the structure of the TSDF metadata, by grouping common values. For the input the list of dictionaries
    corresponds to a list of "flat" metadata dictionaries. The output is a list of dictionaries (potentially of length 1) that contain
    the metadata in a tree structure. The tree structure is created by grouping the common values in the metadata.
    The grouping is done recursively, until no more grouping is possible.

    :param metadatas: List of dictionaries containing the metadata.

    :return: List of dictionaries containing the metadata in a tree structure.
    """

    if len(metadatas) == 0:
        return []
    if len(metadatas) == 1:
        return metadatas

    overlap_per_key: Dict[str, List[dict]] = {}  # Overlap for each key
    final_metadata: List[dict] = []  # The metadata that is left to be processed

    for key in get_all_keys(metadatas):
        overlap_per_key[key] = calculate_max_overlap(metadatas, key)

    max_key = max_len_key(overlap_per_key)

    first_group = overlap_per_key[max_key]
    second_grop = [meta for meta in metadatas if meta not in first_group]

    # Handle the first group
    first_overlap = extract_common_fields(first_group)
    if len(first_group) > 0:
        first_overlap["sensors"] = calculate_ovelaps_rec(first_group)
    final_metadata.append(first_overlap)

    # Handle the rest of the elements
    second_overlap = calculate_ovelaps_rec(second_grop)
    final_metadata.extend(second_overlap)

    return final_metadata


def get_all_keys(metadatas: List[Dict[str, Any]]) -> List[str]:
    """
    Get all the keys from the metadata files.

    :param metadatas: List of dictionaries containing the metadata.

    :return: List of keys.
    """
    keys: List[str] = []
    for meta in metadatas:
        keys.extend(meta.keys())
    return list(set(keys))


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


def calculate_max_overlap(
    meta_files: List[Dict[str, Any]], meta_key: str
) -> List[Dict[str, Any]]:
    """
    Calculate the maximum overlap between the metadata files, for a specific key.
    It returns the biggest group of dictionaries that contain the same value for the given meta_key.

    :param meta_files: List of dictionaries containing the metadata.
    :param meta_key: The key for which the overlap is calculated.

    :return: List of dictionaries containing the metadata.
    """
    values: Dict[
        str, List[Dict[str, Any]]
    ] = (
        {}
    )  # Key: a value for the given meta_key, Value: list of metadata files that have that value
    for meta in meta_files:
        if meta_key in meta.keys():
            curr_value = str(meta[meta_key])
            if curr_value not in values.keys():
                values[curr_value] = [meta]
            else:
                values[curr_value].append(meta)

    max_key = max_len_key(values)
    return values[max_key]


def max_len_key(elements: Dict[str, List[Dict[str, Any]]]) -> str:
    """
    Return the key in a dictionary that has the longest list as a value.

    :param elements: Dictionary containing the elements.

    :return: The key that has the longest list as a value.
    """
    return max(elements, key=lambda x: len(elements[x]))
