import json
from typing import Any, Dict, List

from tsdf import constants
from tsdf.tsdf_metadata import TSDFMetadata


def read_data(data: Any) -> List[TSDFMetadata]:
    """
    Function used to parse the JSON object containing TSDF metadata. It returns a
    list of TSDFMetadata objects, where each object describes formatting of a binary file.
    """

    # Check if the version is supported
    version = data["metadata_version"]
    assert version in constants.SUPPORTED_VERSIONS, f"TSDF file version {version} not supported."

    defined_properties: Dict[str, Any] = {}
    return _read_struct(data, defined_properties.copy(), version)


def _read_struct(data: Any, defined_properties: Dict[str, Any], version: str) -> List[TSDFMetadata]:
    """ Recursive method used to parse the TSDF metadata in a hierarchical order (from the root towards the leaves)."""
    all_streams:List[TSDFMetadata] = []
    remaining_data = {}
    leaf:bool = True

    # 1) Map all the values provided at the current level of the TSDF structure.
    for key, value in data.items():
        if _is_mandatory_type(key, version):
            defined_properties[key] = value
        elif not _contains_file_name(value):
            defined_properties[key] = value
        else:
            leaf = False
            remaining_data[key] = value

    # 2) If the current element is a leaf in the structure, convert it into a TSDFMetadata object.
    if leaf:
        all_streams.append(TSDFMetadata(defined_properties))

    # 3) If the current element is not a leaf, `remaining_data`` will contain lower levels of the TSDF structure.
    # Extend the mapping recursively with values provided at those levels.
    for key, value in remaining_data.items():
        if _is_a_list(value):
            for each_value in value:
                all_streams += _read_struct(each_value, defined_properties.copy(), version)
        else:
            all_streams += _read_struct(value, defined_properties.copy(), version)


    return all_streams


def _is_mandatory_type(key:str, version:str) -> bool:
    """
    Function returns True if the field that corresponds to the
    key is mandatory for the given TSDF version, otherwise it returns False.
    """
    return True if key in constants.MANDATORY_KEYS[version] else False


def _contains_file_name(value) -> bool:
    """
    Function return True if the field contains the "file_name" field, 
    and thus, represents nested data elements.
    otherwise it returns False.
    """
    return "file_name" in json.dumps(value)

def _is_a_list(value) -> bool:
    """ Function returns True if the value is a list, otherwise it returns False."""
    return isinstance(value, list)


def _check_tsdf_mandatory_fields(dictionary: Dict[str, Any]) -> None:
    """
    Verifies that all the mandatory properties for MSDF metadata are provided, and are in the right format.
    """
    version = dictionary["metadata_version"]
    for key in constants.MANDATORY_KEYS[version]:
        assert key in dictionary.keys(), f"TSDF structure is missing key '{key}'"
    assert len(dictionary["units"]) == len(dictionary["channels"]), \
        "TSDF structure requires equal number of 'units' and 'channels'"

    for key, value in dictionary.items():
        _check_tsdf_property_format(key, value, version)

def _check_tsdf_property_format(key:str, value, version:str) -> None:
    """
    Function checks whether the value of the mandatory TSDF field specified by the key
    is of the expected data format.\\
    `Note: If the key is not mandatory the function does not perform any checks.`
    """
    if not _is_mandatory_type(key, version):
        return

    index = constants.MANDATORY_KEYS[version].index(key)
    type_name = constants.MANDATORY_KEYS_VALUES[version][index]

    assert isinstance(value,constants.KNOWN_TYPES[type_name]), f"The given value for {key} is not in the expected ({type_name}) format."
