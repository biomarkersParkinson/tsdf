"""
Module for reading and writing binary files associated with TSDF.

Reference: https://arxiv.org/abs/2211.11294
"""

import os
import numpy as np
from tsdf import numpy_utils 
from tsdf import tsdfmetadata


def load_binary_from_metadata(
    metadata_dir: str, metadata: 'tsdfmetadata.TSDFMetadata', start_row: int = 0, end_row: int = -1
) -> np.ndarray:
    """
    Use metadata properties to load and return numpy array from a binary file.

    :param metadata_dir: path to the directory containing the TSDF metadata files.
    :param metadata: TSDFMetadata object.
    :param start_row: (optional) first row to load.
    :param end_row: (optional) last row to load. If -1, load all rows.

    :return: numpy array containing the data."""
    bin_path = os.path.join(metadata_dir, metadata.file_name)
    return _load_binary_file(
        bin_path,
        metadata.data_type,
        metadata.bits,
        metadata.endianness,
        metadata.rows,
        len(metadata.channels),
        start_row,
        end_row,
    )


def _load_binary_file(
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

    s_endianness = numpy_utils.endianness_tsdf_to_numpy(endianness)
    s_type = numpy_utils.data_type_tsdf_to_numpy(data_type)
    s_n_bytes = numpy_utils.bytes_tsdf_to_numpy(n_bits)
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
