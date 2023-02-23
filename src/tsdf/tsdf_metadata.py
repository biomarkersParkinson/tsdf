import os
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

    _source_path: str
    """ A reference to the source path, so we don't need it again when reading associated binary files """

    def __init__(self, dictionary: Dict[str, Any], source_path: str) -> None:
        """
        The default constructor takes a dictionary as an argument and creates each
        field as a separate property.\\
        `Both, mandatory and non-mandatory fields are stored as object properties.`
        """
        self._source_path = source_path

        io_metadata.check_tsdf_mandatory_fields(dictionary)
        for key, value in dictionary.items():
            setattr(self, key, value)

    def load_binary(self):
        """TODO"""
        metadata_dir = os.path.join(os.path.split(self._source_path)[0])
        return io.load_binary_from_metadata(metadata_dir, self)
