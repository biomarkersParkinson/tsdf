import json
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
