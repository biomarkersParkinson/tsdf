import os
import copy
from typing import Any, Dict, List
from tsdf import io, io_metadata


class TSDFMetadataFieldError(Exception):
    "Raised when the TSDFMetadata is missing an obligatory field."
    pass


class TSDFMetadataFieldValueError(Exception):
    "Raised when a TSDFMetadata field is wrongly annotated."
    pass


class TSDFMetadata:
    """Structure that provides metadata needed for reading a data stream."""

    metadata_version: str
    study_id: str
    subject_id: str
    device_id: str
    start_iso8601: str
    end_iso8601: str
    file_name: str
    rows: int
    channels: List[str]
    units: List[str]
    data_type: str
    bits: int
    endianness: str
    # metadata_hierarchy: List[str]
    # TODO: The idea was to have a property to store the hierarchy of the metadata file.
    # It contains the list of properties that lead to the file_name.
    # However, it is challenging to track the indexes in this structure,
    # e.g., it was the second element in the list under label "sensors".
    file_dir_path: str
    source_file_name: str
    """ A reference to the source path, so we don't need it again when reading associated binary files. """

    def __init__(
        self, dictionary: Dict[str, Any], dir_path: str, file_name: str = ""
    ) -> None:
        """
        The default constructor takes a dictionary as an argument and creates each
        field as a separate property.\\
        `Both, mandatory and non-mandatory fields are stored as object properties.`
        """
        io_metadata.check_tsdf_mandatory_fields(dictionary)
        for key, value in dictionary.items():
            setattr(self, key, value)
        self.file_dir_path = dir_path
        self.source_file_name = file_name

    def get_plain_tsdf_dict(self) -> Dict[str, Any]:
        """Method returns the user defined fields needed for the final TSDF file."""
        simple_dict = copy.deepcopy(self.__dict__)
        if simple_dict.get("file_dir_path") != None:
            simple_dict.pop("file_dir_path")
        if simple_dict.get("source_file_name") != None:
            simple_dict.pop("source_file_name")
        return simple_dict

    def load_binary(self):
        """Load the binary file from the same directory where the metadata is saved."""
        return io.load_binary_from_metadata(self.file_dir_path, self)
