"""
Module for writing TSDF files.

Reference: https://arxiv.org/abs/2211.11294
"""

from typing import Any, Dict, List
from tsdf import file_utils
from tsdf import parse_metadata
from tsdf.tsdfmetadata import TSDFMetadata, TSDFMetadataFieldValueError


def write_metadata(metadatas: List[TSDFMetadata], file_name: str) -> None:
    """
    Combine and save the TSDF metadata objects as a json file.

    :param metadatas: List of TSDFMetadata objects to be saved.
    :param file_name: Name of the file to be saved. The file will be saved in the directory of the first TSDFMetadata object in the list.

    :raises TSDFMetadataFieldValueError: if the metadata files cannot be combined (e.g. they have no common fields) or if the list of TSDFMetadata objects is empty.
    """
    if len(metadatas) == 0:
        raise TSDFMetadataFieldValueError(
            "Metadata cannot be saved, as the list of TSDFMetadata objects is empty."
        )

    if len(metadatas) == 1:
        meta = metadatas[0]
        file_utils.write_to_file(
            meta.get_plain_tsdf_dict_copy(), meta.file_dir_path, file_name
        )
        return

    # Ensure that the metadata files can be combined
    parse_metadata.confirm_dir_of_metadata(metadatas)

    plain_meta = [meta.get_plain_tsdf_dict_copy() for meta in metadatas]
    overlap = _extract_common_fields(plain_meta)
    if not overlap:
        raise TSDFMetadataFieldValueError(
            "Metadata files mist have at least one common field. Otherwise, they should be stored separately."
        )

    if len(plain_meta) > 0:
        overlap["sensors"] = _calculate_ovelaps_rec(plain_meta)
    file_utils.write_to_file(overlap, metadatas[0].file_dir_path, file_name)


def _extract_common_fields(metadatas: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Extract the fields that are the same for all the metadata files.
    A new dict is created and the fields are removed from the original dictionaries.

    :param metadatas: List of dictionaries containing the metadata.

    :return: Dictionary containing the common fields.
    """
    meta_overlap: dict = {}

    # Return empty dict if metadatas is empty
    if len(metadatas) == 0:
        return meta_overlap
    if len(metadatas) == 1:
        return metadatas.pop(0)
    init_metadata = metadatas[0]
    for key, value in init_metadata.items():
        key_in_all = True
        for curr_meta in metadatas[1:]:
            if key not in curr_meta.keys() or curr_meta[key] != value:
                key_in_all = False
        if key_in_all:
            meta_overlap[key] = value
    for key, _ in meta_overlap.items():
        for meta_dict in metadatas:
            meta_dict.pop(key)
    return meta_overlap


def _calculate_ovelaps_rec(metadatas: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    A recursive call that optimises the structure of the TSDF metadata, by grouping common values. For the input the list of dictionaries
    corresponds to a list of "flat" metadata dictionaries. The output is a list of dictionaries (potentially of length 1) that contain
    the metadata in a tree structure. The tree structure is created by grouping the common values in the metadata.
    The grouping is done recursively, until no more grouping is possible.

    :param metadatas: List of dictionaries containing the metadata.

    :return: List of dictionaries containing the metadata in a tree structure.
    """

    if len(metadatas) == 0:
        return []
    if len(metadatas) == 1:
        return metadatas

    overlap_per_key: Dict[str, List[dict]] = {}  # Overlap for each key
    final_metadata: List[dict] = []  # The metadata that is left to be processed

    for key in _get_all_keys(metadatas):
        overlap_per_key[key] = calculate_max_overlap(metadatas, key)

    max_key = max_len_key(overlap_per_key)

    first_group = overlap_per_key[max_key]
    second_grop = [meta for meta in metadatas if meta not in first_group]

    # Handle the first group
    first_overlap = _extract_common_fields(first_group)
    if len(first_group) > 0:
        first_overlap["sensors"] = _calculate_ovelaps_rec(first_group)
    final_metadata.append(first_overlap)

    # Handle the rest of the elements
    second_overlap = _calculate_ovelaps_rec(second_grop)
    final_metadata.extend(second_overlap)

    return final_metadata


def _get_all_keys(metadatas: List[Dict[str, Any]]) -> List[str]:
    """
    Get all the keys from the metadata files.

    :param metadatas: List of dictionaries containing the metadata.

    :return: List of keys.
    """
    keys: List[str] = []
    for meta in metadatas:
        keys.extend(meta.keys())
    return list(set(keys))


def calculate_max_overlap(
    meta_files: List[Dict[str, Any]], meta_key: str
) -> List[Dict[str, Any]]:
    """
    Calculate the maximum overlap between the metadata files, for a specific key.
    It returns the biggest group of dictionaries that contain the same value for the given meta_key.

    :param meta_files: List of dictionaries containing the metadata.
    :param meta_key: The key for which the overlap is calculated.

    :return: List of dictionaries containing the metadata.
    """
    values: Dict[
        str, List[Dict[str, Any]]
    ] = (
        {}
    )  # Key: a value for the given meta_key, Value: list of metadata files that have that value
    for meta in meta_files:
        if meta_key in meta.keys():
            curr_value = str(meta[meta_key])
            if curr_value not in values.keys():
                values[curr_value] = [meta]
            else:
                values[curr_value].append(meta)

    max_key = max_len_key(values)
    return values[max_key]


def max_len_key(elements: Dict[str, List[Dict[str, Any]]]) -> str:
    """
    Return the key in a dictionary that has the longest list as a value.

    :param elements: Dictionary containing the elements.

    :return: The key that has the longest list as a value.
    """
    return max(elements, key=lambda x: len(elements[x]))
