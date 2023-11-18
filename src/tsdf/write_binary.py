"""
Module for writing binary files associated with TSDF.

Reference: https://arxiv.org/abs/2211.11294
"""

import os
from typing import Any, Dict
import numpy as np
from tsdf import numpy_utils 

from tsdf.tsdfmetadata import TSDFMetadata



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

def verify_metadata_compatibility(metadata: dict, data: np.ndarray) -> bool:
    """
    Verify if the metadata is compatible with the data.

    :param metadata: dictionary containing the metadata.
    :param data: NumPy array containing the data.

    :return: True if the metadata is compatible with the data, False otherwise.
    """
    compatible = True
    compatible &= len(metadata["channels"]) == data.shape[1]
    
    return compatible
        


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
    if (not verify_metadata_compatibility(metadata, data)):
        raise ValueError("Metadata is not compatible with the data.")
    path = os.path.join(file_dir, file_name)
    data.tofile(path)
    metadata.update(_get_metadata_from_ndarray(data))
    metadata.update({"file_name": file_name})

    return TSDFMetadata(metadata, file_dir)
