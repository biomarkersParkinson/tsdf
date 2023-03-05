import json
import os
import sys
from typing import Dict, List
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
from tsdf.tsdf_metadata import TSDFMetadata


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


def get_metadata_from_ndarray(data: np.ndarray) -> dict:
    """Retrieve metadata information encoded in the NumPy array."""

    metadata = {
        "data_type": data_type_numpy_to_tsdf(data),
        "bits": bits_numpy_to_tsdf(data),
        "endianness": endianness_numpy_to_tsdf(data),
        "rows": rows_numpy_to_tsdf(data),
    }
    return metadata


def save_binary_file(
    file_dir: str, file_name: str, data: np.ndarray, metadata: dict
) -> TSDFMetadata:
    """Save binary file based on the provided NumPy array."""
    path = os.path.join(file_dir, file_name)
    data.tofile(path)
    metadata.update(get_metadata_from_ndarray(data))
    metadata.update({"file_name": file_name})

    return TSDFMetadata(metadata, file_dir)


def confirm_dir_of_metadata(metadatas: List[TSDFMetadata]) -> bool:
    """The method is used to confirm whether all the metadata files are expected in the same directory."""
    metadata_iter = iter(metadatas)
    init_metadata = next(metadata_iter)

    for curr_metadata in metadatas:
        if init_metadata.file_dir_path != curr_metadata.file_dir_path:
            raise Exception(
                "Metadata files have to be in the same folder to be combined."
            )
        if init_metadata.file_name == curr_metadata.file_name:
            raise Exception(
                "Two metadata objects cannot reference the same binary file (file_name)."
            )

    return True


def save_metadata(metadatas: List[TSDFMetadata], file_name: str) -> None:
    """Combine and save the TSDF metadata objects as a json file."""
    if metadatas.__sizeof__ == 0:
        raise Exception(
            "Metadata cannot be saved, as the list of TSDFMetadata objects is empty."
        )

    if metadatas.__sizeof__ == 1:
        meta = metadatas[0]
        write_to_file(meta.__dict__, meta.file_dir_path, file_name)

    confirm_dir_of_metadata(metadatas)
    print(dir(metadatas[0]))
    # overlap = get_overlap(metadatas, dict(metadatas[0]))


def get_overlap(metadatas: List[TSDFMetadata], keys: List[str]) -> List[int]:
    for meta in metadatas:
        print("x")

    return []


def write_to_file(dict: dict, dir_path: str, file_name: str) -> None:
    path = os.path.join(dir_path, file_name)
    with open(path, "w") as convert_file:
        convert_file.write(json.dumps(dict))
