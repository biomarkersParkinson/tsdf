import json
import os
from typing import Dict
import numpy as np
from tsdf import io_metadata
from tsdf.tsdf_metadata import TSDFMetadata

def load_file(file) -> Dict[str, TSDFMetadata]:
    """ Loads a TSDF metadata file, returns a dictionary 
    
    Reference: https://arxiv.org/abs/2211.11294
    """
    
    # The data is isomorphic to a JSON
    data = json.load(file)

    # Parse the data and verify that it complies with TSDF requirements
    return io_metadata.read_data(data)

  
def load_from_path(path: str) -> Dict[str, TSDFMetadata]:
    """ Loads a TSDF metadata file, returns a dictionary 
    
    Reference: https://arxiv.org/abs/2211.11294
    """
    # The data is isomorphic to a JSON
    with open(path) as file:
        data = json.load(file)
    
    # Parse the data and verify that it complies with TSDF requirements
    return io_metadata.read_data(data)

def load_string(json_str) -> Dict[str, TSDFMetadata]:
    """ Loads a TSDF metadata string, returns a dictionary
    
    Reference: https://arxiv.org/abs/2211.11294
    """

    # The data is isomorphic to a JSON
    data = json.loads(json_str)
    
    # Parse the data and verify that it complies with TSDF requirements
    return io_metadata.read_data(data)

def load_binary_from_metadata(metadata_dir: str, metadata: TSDFMetadata) -> np.ndarray:
    """ Use metadata properties to load and return numpy array from a binary file
    """
    bin_path = os.path.join(metadata_dir, metadata.file_name)
    return load_binary_file(bin_path, metadata.data_type, metadata.bits,
        metadata.endianness, metadata.rows, len(metadata.channels))

def load_binary_file(file_path: str, data_type: str, n_bits: int, endianness: str,
        n_rows: int, n_columns: int) -> np.ndarray:
    """ Use provided parameters to load and return a numpy array from a binary file
    """

    # Build format string that numpy understands
    dtype_mapping = {
        'float': 'f',
        'int': 'i'
    }
    s_endianness = '<' if endianness == 'little' else '>'
    s_type = dtype_mapping[data_type]
    s_n_bytes = str(n_bits // 8)
    format_string = ''.join([s_endianness, s_type, s_n_bytes])

    # Load the data and reshape
    with open(file_path, 'rb') as fid:
        values = np.fromfile(fid, dtype=format_string)
        if n_columns > 1:
            values = values.reshape((-1, n_columns))

    # Check whether the number of rows matches the metadata
    if values.shape[0] != n_rows:
        raise Exception("Number of rows doesn't match file length.")

    return values
