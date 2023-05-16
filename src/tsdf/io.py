import json
import os
import sys
from typing import Any, Dict, List
import numpy as np
from tsdf import io_metadata
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

    Reference: https://arxiv.org/abs/2211.11294
    """

    # The data is isomorphic to a JSON
    data = json.load(file)

    abs_path = os.path.realpath(file.name)

    # Parse the data and verify that it complies with TSDF requirements
    return io_metadata.read_data(data, abs_path)


def load_metadata_from_path(path: str) -> Dict[str, TSDFMetadata]:
    """Loads a TSDF metadata file, returns a dictionary

    Reference: https://arxiv.org/abs/2211.11294
    """
    # The data is isomorphic to a JSON
    with open(path, "r") as file:
        data = json.load(file)

    abs_path = os.path.realpath(path)
    # Parse the data and verify that it complies with TSDF requirements
    return io_metadata.read_data(data, abs_path)


def load_metadata_string(json_str) -> Dict[str, TSDFMetadata]:
    """Loads a TSDF metadata string, returns a dictionary

    Reference: https://arxiv.org/abs/2211.11294
    """

    # The data is isomorphic to a JSON
    data = json.loads(json_str)

    # Parse the data and verify that it complies with TSDF requirements
    return io_metadata.read_data(data, "")


def load_binary_from_metadata(metadata_dir: str, metadata: TSDFMetadata) -> np.ndarray:
    """Use metadata properties to load and return numpy array from a binary file"""
    bin_path = os.path.join(metadata_dir, metadata.file_name)
    return load_binary_file(
        bin_path,
        metadata.data_type,
        metadata.bits,
        metadata.endianness,
        metadata.rows,
        len(metadata.channels),
    )


def load_binary_file(
    bin_file_path: str,
    data_type: str,
    n_bits: int,
    endianness: str,
    n_rows: int,
    n_columns: int,
) -> np.ndarray:
    """Use provided parameters to load and return a numpy array from a binary file"""

    s_endianness = endianness_tsdf_to_numpy(endianness)
    s_type = data_type_tsdf_to_numpy(data_type)
    s_n_bytes = bytes_tsdf_to_numpy(n_bits)
    format_string = "".join([s_endianness, s_type, s_n_bytes])

    # Load the data and reshape
    with open(bin_file_path, "rb") as fid:
        values = np.fromfile(fid, dtype=format_string)
        if n_columns > 1:
            values = values.reshape((-1, n_columns))

    # Check whether the number of rows matches the metadata
    if values.shape[0] != n_rows:
        raise Exception("Number of rows doesn't match file length.")

    return values


def get_metadata_from_ndarray(data: np.ndarray) -> Dict[str, Any]:
    """Retrieve metadata information encoded in the NumPy array."""

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
    """Save binary file based on the provided NumPy array."""
    path = os.path.join(file_dir, file_name)
    data.tofile(path)
    metadata.update(get_metadata_from_ndarray(data))
    metadata.update({"file_name": file_name})

    return TSDFMetadata(metadata, file_dir)


def write_metadata(metadatas: List[TSDFMetadata], file_name: str) -> None:
    """Combine and save the TSDF metadata objects as a json file."""
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

    overlap["sensors"] = calculate_ovelaps_rec(plain_meta)
    write_to_file(overlap, metadatas[0].file_dir_path, file_name)


def extract_common_fields(metadatas: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Extract the fields that are the same for all the metadata files.
    A new dict is created and the fields are removed from the original dictionaries."""
    meta_overlap: Dict[str, Any] = {}

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


def calculate_ovelaps_rec(
    metadatas: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """TODO: A recursive call that should optimise the structure of the TSDF metadata, by grouping common values."""
    overlap_per_key: Dict[str, List[Dict[str, Any]]] = {} # Overlap for each key
    final_metadata: List[Dict[str, Any]] = [] # The metadata that is left to be processed

    for key in get_all_keys(metadatas):
        overlap_per_key[key] = calculate_max_overlap(metadatas, key)

    max_key = max_len_key(overlap_per_key)

    final_metadata.append(group_by_key(metadatas, max_key))

    # final_metadata.append(calculate_ovelaps_rec()

# ...
    return final_metadata


def get_all_keys(metadatas: List[Dict[str, Any]]) -> List[str]:
    """Get all the keys from the metadata files."""
    keys:List[str] = []
    for meta in metadatas:
        keys.extend(meta.keys())
    return list(set(keys))

def write_to_file(dict: Dict[str, Any], dir_path: str, file_name: str) -> None:
    """Write a dictionary to a json file."""
    path = os.path.join(dir_path, file_name)
    with open(path, "w") as convert_file:
        convert_file.write(json.dumps(dict))


def calculate_max_overlap(meta_files: List[Dict[str, Any]], max_key: str) -> List[Dict[str, Any]]:
    """Calculate the maximum overlap between the metadata files, for a specific key and return the results as a dictionary."""
    values : Dict[str, List[Dict[str, Any]]] = {}
    for meta in meta_files:
        curr = meta[max_key]
        if curr not in values.keys():
            values[curr] = [meta]
        values[curr].append(meta)
        
    max_key = max_len_key(values)
    return values[max_key]




def max_len_key(elements: Dict[str, List[Dict[str, Any]]]) -> str:
    """Return the key that has the longest list as a value."""
    return max(elements, key=lambda x: len(elements[x]))


def group_by_key(meta_files: List[Dict[str, Any]], key: str) -> Any:
    """Group the metadata files by a specific key and return the results as a dictionary."""
    return meta_files
