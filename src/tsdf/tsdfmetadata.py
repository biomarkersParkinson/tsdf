import copy
from typing import Any, Dict, List
from datetime import datetime
from dateutil import parser

from tsdf import parse_metadata

class TSDFMetadataFieldError(Exception):
    "Raised when the TSDFMetadata is missing an obligatory field."
    @classmethod
    def missing_field(cls, field_name: str):
        message = f"Value for the obligatory TSDF field '{field_name}' is missing in the provided TSDF metadata file."
        return cls(message)


class TSDFMetadataFieldValueError(Exception):
    "Raised when a TSDFMetadata field is wrongly annotated."
    pass


class TSDFMetadata:
    """Structure that provides metadata needed for reading a data stream."""

    metadata_version: str
    """Version of the TSDF metadata file."""
    study_id: str
    """Study ID."""
    subject_id: str
    """Subject ID."""
    device_id: str
    """Device ID."""
    start_iso8601: str
    """Start time of the recording in ISO8601 format."""
    end_iso8601: str
    """End time of the recording in ISO8601 format."""
    file_name: str
    """Name of the binary file containing the data."""
    rows: int
    """Number of rows in the binary file."""
    channels: List[str]
    """List of channels in the binary file."""
    units: List[str]
    """List of units for each channel in the binary file."""
    data_type: str
    """Data type of the binary file."""
    bits: int
    """Number of bits per sample in the binary file."""
    endianness: str
    """Endianness of the binary file."""

    file_dir_path: str
    """ A reference to the directory path, so we don't need it again when reading associated binary files. """
    metadata_file_name: str #TODO: do we need this?? / is it used?
    """ A reference to the source path, so we don't need it again when reading associated binary files. """

    def __init__(
        self, dictionary: Dict[str, Any], dir_path: str, metadata_file_name: str = "", do_validate: bool = True
    ) -> None:
        """
        The default constructor takes a dictionary as an argument and creates each
        field as a separate property.\\
        `Both, mandatory and non-mandatory fields are stored as object properties.`

        :param dictionary: dictionary containing TSDF metadata.
        :param dir_path: path to the directory where the metadata file is stored.
        :param metadata_file_name: (optional) name of the metadata file.
        :param do_validate: (optional) flag to validate the metadata.
        """

        # Copy the attributes from the dictionary to the object
        for key, value in dictionary.items():
            setattr(self, key, value)
        self.file_dir_path = dir_path
        self.metadata_file_name = metadata_file_name

        # Validate the metadata
        if do_validate:
            if not self.validate():
                raise TSDFMetadataFieldValueError("The provided metadata is invalid.")


    def validate(self) -> bool:
        isValid: bool = True

        # Validate presence of mandatory fields
        dict = self.get_plain_tsdf_dict_copy()
        isValid = isValid and parse_metadata.contains_tsdf_mandatory_fields(dict)

        # Validate datetimes
        isValid = isValid and parse_metadata.validate_datetimes(self)

        return isValid

    def get_plain_tsdf_dict_copy(self) -> Dict[str, Any]:
        """
        Method returns the a copy of the dict containing fields needed for the TSDF file.

        :return: a copy of the dict containing fields needed for the TSDF file.
        """
        simple_dict = copy.deepcopy(self.__dict__)
        if simple_dict.get("file_dir_path") is not None:
            simple_dict.pop("file_dir_path")
        if simple_dict.get("metadata_file_name") is not None:
            simple_dict.pop("metadata_file_name")
        return simple_dict

    def set_start_datetime(self, date_time: datetime) -> None:
        """
        Sets the start date of the recording in ISO8601 format.
        :param date_time: datetime object containing the start date.
        """
        self.start_iso8601 = date_time.isoformat()

    def get_start_datetime(self) -> datetime:
        """
        Returns the start date of the recording as a datetime object.
        :return: datetime object containing the start date.
        """
        return parser.parse(self.start_iso8601)

    def set_end_datetime(self, date_time: datetime) -> None:
        """
        Sets the end date of the recording in ISO8601 format.
        :param date_time: datetime object containing the end date.
        """
        self.end_iso8601 = date_time.isoformat()

    def get_end_datetime(self) -> datetime:
        """
        Returns the end date of the recording as a datetime object.
        :return: datetime object containing the end date.
        """
        return parser.parse(self.end_iso8601)

    start = property(get_start_datetime, set_start_datetime, doc=
        """
        Start time of the recording.
        """)

    end = property(get_end_datetime, set_end_datetime, doc=
        """
        End time of the recording.
        """)
