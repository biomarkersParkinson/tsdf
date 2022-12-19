import json
from flatten_json import flatten
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
    flat_data = flatten(data)
    for key in MANDATORY_KEYS[version]:
        assert any(key in k for k in flat_data.keys()), f"Missing key: {key}"
        # Why is this not the more straightforward
        # assert key in flat_data.keys()
        # ?
        #
        # Because the dictionary is flattened, and the keys' names are composed.
        # For instance, a key could be `multi-day_session_0_sensors_0_file_name`