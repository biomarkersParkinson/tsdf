import json
from tsdf.constants import *

def load(file):
    """ Loads a TSDF metadata file, returns a dictionary """

    # The data is isomorphic to a JSON
    data = json.load(file)
    
    # Check that it complies with TSDF requirements
    _check(data)

    return data

def loads(s):
    """ Loads a TSDF metadata string, returns a dictionary """

    # The data is isomorphic to a JSON
    data = json.loads(s)
    
    # Check that it complies with TSDF requirements
    _check(data)

    return data

def _check(data):
    """ Fails if something is suspicious """

    # Check if the version is supported
    version = data["metadata_version"]
    assert version in SUPPORTED_VERSIONS, f"TSDF file version {version} not supported."

    # Check that mandatory keys are present
    # TODO: move to constants.py
    mandatory_keys = ["subject_id","study_id","device_id",
                      "endianness","metadata_version","data_type",
                      "bits", "rows","channels",
                      "units","file_name","start_iso8601","end_iso8601"]

    # TODO: the snippet below only tests keys at depth 1. As a consequence, it 
    # works fine for flat.json, but fails with hierarchical.json
    #
    # for key in mandatory_keys:
    #    data[key] # Throws error if a key is not present