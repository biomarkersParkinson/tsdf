import json
import os
import numpy as np
from typing import List
from tsdf.tsdf_metadata import TSDFMetadata

def load_file(file) -> List[TSDFMetadata]:
    """ Loads a TSDF metadata file, returns a dictionary 
    
    Reference: https://arxiv.org/abs/2211.11294
    """

    # The data is isomorphic to a JSON
    data = json.load(file)

    # Parse the data and verify that it complies with TSDF requirements
    return TSDFMetadata.read_data(data)

  
def load_from_path(path: str) -> List[TSDFMetadata]:
    """ Loads a TSDF metadata file, returns a dictionary 
    
    Reference: https://arxiv.org/abs/2211.11294
    """
    # The data is isomorphic to a JSON
    with open(path) as file:    
        data = json.load(file)
    
    # Parse the data and verify that it complies with TSDF requirements
    return TSDFMetadata.read_data(data)

def load_string(json_str) -> List[TSDFMetadata]:
    """ Loads a TSDF metadata string, returns a dictionary
    
    Reference: https://arxiv.org/abs/2211.11294
    """

    # The data is isomorphic to a JSON
    data = json.loads(json_str)
    
    # Parse the data and verify that it complies with TSDF requirements
    return TSDFMetadata.read_data(data)

def load_binary_from_metadata(metadata_dir: str, metadata: TSDFMetadata) -> np.ndarray:
    bin_path = os.path.join(metadata_dir, metadata.file_name)
    return load_binary_file(bin_path, metadata.data_type, metadata.bits,
        metadata.endianness, len(metadata.channels))

def load_binary_file(file_path: str, type: str, nbits: int, endianness: str, 
        ncolumns: int) -> np.ndarray:
    dtype_mapping = {
        'float': 'f',
        'int': 'i'
    }
    s_endianness = '<' if endianness == 'little' else '>'
    s_type = dtype_mapping[type]
    s_nbytes = str(nbits // 8)
    format_string = ''.join([s_endianness, s_type, s_nbytes])

    with open(file_path, 'rb') as fid:
        values = np.fromfile(fid, dtype=format_string)
        if ncolumns > 1:
            values = values.reshape((-1, ncolumns))

    return values
