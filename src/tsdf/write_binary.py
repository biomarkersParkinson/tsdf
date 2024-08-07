"""
Module for writing binary files associated with TSDF.

Reference: https://arxiv.org/abs/2211.11294
"""

import os
from typing import Any, Dict, List
import numpy as np
import pandas as pd
from tsdf import numpy_utils

from tsdf.tsdfmetadata import TSDFMetadata


def write_dataframe_to_binaries(
    file_dir: str, df: pd.DataFrame, metadatas: List[TSDFMetadata]
) -> None:
    """
    Save binary file based on the provided pandas DataFrame.

    :param file_dir:    path to the directory where the file will be saved.
    :param df:          pandas DataFrame containing the data.
    :param metadatas:   list of metadata objects to be saved, also contains
                        channels to be retrieved from dataframe.
    """
    for metadata in metadatas:
        file_name = metadata.file_name
        path = os.path.join(file_dir, file_name)
        
        # Write
        data = df[metadata.channels].to_numpy() # TODO: derive channels from dataframe or use specified in metadata? Also for file_name?
        data.tofile(path)

        # Update metadata with data properties
        data_props = _get_metadata_from_ndarray(data)
        for key in data_props:
            metadata.__setattr__(key, data_props[key])


def _get_metadata_from_ndarray(data: np.ndarray) -> Dict[str, Any]:
    """
    Retrieve metadata information encoded in the NumPy array.

    :param data: NumPy array containing the data.

    :return: dictionary containing the metadata.
    """

    metadata = {
        "data_type": numpy_utils.data_type_numpy_to_tsdf(data),
        "bits": numpy_utils.bits_numpy_to_tsdf(data),
        "endianness": numpy_utils.endianness_numpy_to_tsdf(data),
        "rows": numpy_utils.rows_numpy_to_tsdf(data),
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
    metadata.update(_get_metadata_from_ndarray(data))
    metadata.update({"file_name": file_name})

    return TSDFMetadata(metadata, file_dir)
