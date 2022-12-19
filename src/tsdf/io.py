import json
from tsdf.constants import *

def load(file):
    """ Loads a TSDF metadata file, returns a dictionary 
    
    Reference: https://arxiv.org/abs/2211.11294
    """

    # The data is isomorphic to a JSON
    data = json.load(file)
    
    # Check that it complies with TSDF requirements
    _check(data)

    return data

def loads(s):
    """ Loads a TSDF metadata string, returns a dictionary
    
    Reference: https://arxiv.org/abs/2211.11294
    """

    # The data is isomorphic to a JSON
    data = json.loads(s)
    
    # Check that it complies with TSDF requirements
    _check(data)

    return data

def _check(data):
    """ Fails if something goes not according to the format
    
    Reference: https://arxiv.org/abs/2211.11294
    """

    # Check if the version is supported
    version = data["metadata_version"]
    assert version in SUPPORTED_VERSIONS, f"TSDF file version {version} not supported."

    # Check that mandatory keys are present
    # TODO: the snippet below only tests keys at depth 1. As a consequence, it 
    # works fine for flat.json, but fails with hierarchical.json
    # for key in MANDATORY_KEYS[version]:
    #    data[key] # Throws error if a key is not present