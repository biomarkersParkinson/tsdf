from typing import Any, Dict, List

from tsdf import constants

class TSDFMetadata:
    """Structure that should provide metadata needed for reading a data stream."""
    subject_id: str
    study_id: str
    device_id: str
    endianness: str
    metadata_version: str
    start_iso8601: str
    end_iso8601: str
    rows: int
    file_name: str
    channels: List[str]
    units: List[str]
    data_type: str
    bits: int

    def __init__(self, dictionary: Dict[str, Any], version) -> None:
        """ The default constructor takes a dictionary as an argument and creates each mandatory
            field as a separate property. The non-mandatory fields are stored as a dict property
            (additional_properties). """
        for key in constants.MANDATORY_KEYS[version]:
            assert key in dictionary.keys(), f"TSDF structure is missing key '{key}'"
        assert len(dictionary["units"]) == len(dictionary["channels"]), \
            "TSDF structure requires equal number of 'units' and 'channels'"

        for key, value in dictionary.items():
            setattr(self, key, value)


    @staticmethod
    def read_data(data):
        """ Method used to parse the JSON object containing TSDF metadata. """
 
        # Check if the version is supported
        version = data["metadata_version"]
        assert version in constants.SUPPORTED_VERSIONS, f"TSDF file version {version} not supported."

        defined_properties:dict = {}
        return TSDFMetadata._read_struct(data, defined_properties.copy(), version)


    @staticmethod
    def _read_struct(data, defined_properties, version) -> list:
        """ Recursive method used to parse the TSDF metadata in a hierarchical order (from the root towards the leaves)."""
        all_streams:List[TSDFMetadata] = []

        # First, make a list of all values provided at the current level of the TSDF structure
        for key, value in data.items():
            if key in constants.MANDATORY_KEYS[version]:
                TSDFMetadata._check_format(key, value, version)
                defined_properties[key] = value
            elif isinstance(value, (int,str)):
                defined_properties[key] = value
        leaf:bool = True

        # Second, retrieve values provided at the lower levels of the TSDF structure
        for key, value in data.items():
            if key not in constants.MANDATORY_KEYS[version]:
                if isinstance(value, dict):
                    leaf = False
                    all_streams.append(TSDFMetadata._read_struct(value, defined_properties.copy(), version))
                elif isinstance(value, list): #TODO: Can we have a list of regular elements here? Ideally we would have an obligatory key that allows "nesting"
                    for each_value in value:
                        if isinstance(each_value, dict):
                            leaf = False
                            all_streams.append(TSDFMetadata._read_struct(each_value, defined_properties.copy(), version))

        assert not leaf or "file_name" in defined_properties, "'file_name' was expected in the TSDF metadata."

        if leaf: all_streams.append(TSDFMetadata(defined_properties, version))
        return all_streams


    @staticmethod
    def _check_format(key, value, version):
        """ Checks whether the given value is of the expected format. """
        index = constants.MANDATORY_KEYS[version].index(key)
        type_name = constants.MANDATORY_KEYS_VALUES[version][index]

        assert isinstance(value,constants.KNOWN_TYPES[type_name]), f"The given value for {key} is not in the expected ({type_name}) format."
