"""
Module for parsing TSDF metadata files.

Reference: https://arxiv.org/abs/2211.11294
"""

import os
from typing import Any, Dict, List

from tsdf import constants
from tsdf import tsdfmetadata 

def read_data(data: Any, source_path: str) -> Dict[str, 'tsdfmetadata.TSDFMetadata']:
    """
    Function used to parse the JSON object containing TSDF metadata. It returns a
    list of TSDFMetadata objects, where each object describes formatting of a binary file.

    :param data: JSON object containing TSDF metadata.
    :param source_path: path to the metadata file.

    :return: list of TSDFMetadata objects.
    """

    # Check if the version is supported
    version = data["metadata_version"]
    if not version in constants.SUPPORTED_TSDF_VERSIONS:
        raise tsdfmetadata.TSDFMetadataFieldValueError(f"TSDF file version {version} not supported.")

    defined_properties: Dict[str, Any] = {}
    return _read_struct(data, defined_properties.copy(), source_path, version)


def _read_struct(
    data: Any, defined_properties: Dict[str, Any], source_path, version: str
) -> Dict[str, 'tsdfmetadata.TSDFMetadata']:
    """
    Recursive method used to parse the TSDF metadata in a hierarchical
    order (from the root towards the leaves).

    :param data: JSON object containing TSDF metadata.
    :param defined_properties: dictionary containing all the properties defined at the current level of the TSDF structure.
    :param source_path: path to the metadata file.
    :param version: version of the TSDF used within the file.

    :return: list of TSDFMetadata objects.

    :raises tsdf_metadata.TSDFMetadataFieldError: if the TSDF metadata file is missing a mandatory field.
    """
    all_streams: Dict[str, 'tsdfmetadata.TSDFMetadata'] = {}
    remaining_data = {}
    leaf: bool = True

    # 1) Map all the values provided at the current level of the TSDF structure.
    for key, value in data.items():
        if is_mandatory_type(key, version):
            defined_properties[key] = value
        elif not _contains_file_name(value):
            defined_properties[key] = value
        else:
            leaf = False
            remaining_data[key] = value

    # 2) If the current element is a leaf in the structure, convert it into a TSDFMetadata object.
    if leaf:
        try:
            bin_file_name = defined_properties["file_name"]
            path = os.path.split(source_path)
            file_dir = os.path.join(path[0])
            meta_file_name = path[1]
            all_streams[bin_file_name] = tsdfmetadata.TSDFMetadata(
                defined_properties, file_dir, meta_file_name
            )
        except tsdfmetadata.TSDFMetadataFieldError as exc:
            raise tsdfmetadata.TSDFMetadataFieldError(
                "A property 'file_name' is missing in the TSDF metadata file."
            ) from exc

    # 3) If the current element is not a leaf, `remaining_data`` will contain lower
    # levels of the TSDF structure.
    # Extend the mapping recursively with values provided at those levels.
    for key, value in remaining_data.items():
        if _is_a_list(value):
            for each_value in value:
                all_streams = all_streams | _read_struct(
                    each_value, defined_properties.copy(), source_path, version
                )
        else:
            all_streams = all_streams | _read_struct(
                value, defined_properties.copy(), source_path, version
            )

    return all_streams


def is_mandatory_type(key: str, version: str) -> bool:
    """
    Function returns True if the field that corresponds to the
    key is mandatory for the given TSDF version, otherwise it returns False.

    :param key: key of the TSDF metadata field.
    :param version: version of the TSDF used within the file.

    :return: True if the field is mandatory, otherwise False.
    """
    return True if key in constants.MANDATORY_TSDF_KEYS[version] else False


def _contains_file_name(data: Any) -> bool:
    """
    Function return True if the data contains the "file_name" key,
    and thus, represents nested data elements.
    Otherwise it returns False.

    :param data: data to be checked.

    :return: True if the data contains the "file_name" key, otherwise False.
    """

    if isinstance(data, list):
        for elem in data:
            if _contains_file_name(elem):
                return True

    if not isinstance(data, dict):
        return False

    for key, value in data.items():
        if key == "file_name":
            return True
        if _contains_file_name(value):
            return True
    return False


def _is_a_list(value) -> bool:
    """
    Function returns True if the value is a list, otherwise it returns False.

    :param value: value to be checked.

    :return: True if the value is a list, otherwise False.
    """
    return isinstance(value, list)


def contains_tsdf_mandatory_fields(dictionary: Dict[str, Any]) -> bool:
    """
    Verifies that all the mandatory properties for TSDF metadata are provided,
    and are in the right format.

    :param dictionary: dictionary containing TSDF metadata.

    :return: True if the metadata is well formatted.

    :raises tsdf_metadata.TSDFMetadataFieldError: if the TSDF metadata file is missing a mandatory field.
    :raises tsdf_metadata.TSDFMetadataFieldValueError: if the TSDF metadata file contains an invalid value.
    """
    version_key = "metadata_version"
    if not version_key in dictionary.keys():
        raise tsdfmetadata.TSDFMetadataFieldError(f"TSDF structure is missing key '{version_key}'")

    version = dictionary[version_key]
    for key in constants.MANDATORY_TSDF_KEYS[version]:
        if not key in dictionary.keys():
            raise tsdfmetadata.TSDFMetadataFieldError(f"TSDF structure is missing key '{key}'")
    units = "units"
    channels = "channels"
    if len(dictionary[units]) != len(dictionary[channels]):
        raise tsdfmetadata.TSDFMetadataFieldValueError(
            f"TSDF structure requires equal number of {units} and {channels}"
        )

    for key, value in dictionary.items():
        _check_tsdf_property_format(key, value, version)

    return True


def _check_tsdf_property_format(key: str, value, version: str) -> None:
    """
    Function checks whether the value of the mandatory TSDF field specified by the key
    is of the expected data format.\\
    `Note: If the key is not mandatory the function does not perform any checks.`

    :param key: key of the TSDF metadata field.
    :param value: value of the TSDF metadata field.
    :param version: version of the TSDF used within the file.

    :raises tsdf_metadata.TSDFMetadataFieldValueError: if the TSDF metadata file contains an invalid value.
    """
    if not is_mandatory_type(key, version):
        return

    index = constants.MANDATORY_TSDF_KEYS[version].index(key)
    type_name = constants.MANDATORY_TSDF_KEYS_VALUES[version][index]

    if not isinstance(value, constants.KEY_VALUE_TYPES[type_name]):
        raise tsdfmetadata.TSDFMetadataFieldValueError(
            f"The given value for {key} is not in the expected ({type_name}) format."
        )


def get_file_metadata_at_index(
    metadata: Dict[str, 'tsdfmetadata.TSDFMetadata'], index: int
) -> 'tsdfmetadata.TSDFMetadata':
    """
    Returns the metadata object at the position defined by the index.

    :param metadata: dictionary containing TSDF metadata.
    :param index: index of the metadata object to be returned.

    :return: metadata object at the position defined by the index.

    :raises IndexError: if the index is out of range.
    """
    for _key, value in metadata.items():
        if index == 0:
            return value
        index -= 1
    raise IndexError("The index is out of range.")


def confirm_dir_of_metadata(metadatas: List['tsdfmetadata.TSDFMetadata']) -> None:
    """
    The method is used to confirm whether all the metadata files are expected in the same directory.

    :param metadatas: list of metadata objects.

    :raises tsdf_metadata.TSDFMetadataFieldValueError: if the metadata files are not in the same directory or describe the same binaries.
    """
    metadata_iter = iter(metadatas)
    init_metadata = next(metadata_iter)

    for curr_metadata in metadata_iter:
        if init_metadata.file_dir_path != curr_metadata.file_dir_path:
            raise tsdfmetadata.TSDFMetadataFieldValueError(
                "Metadata files have to be in the same folder to be combined."
            )
        if init_metadata.file_name == curr_metadata.file_name:
            raise tsdfmetadata.TSDFMetadataFieldValueError(
                "Two metadata objects cannot reference the same binary file (file_name)."
            )
