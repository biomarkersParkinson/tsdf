from typing import Any, Dict, List

from tsdf import io_metadata

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

    def __init__(self, dictionary: Dict[str, Any]) -> None:
        """
        The default constructor takes a dictionary as an argument and creates each
        field as a separate property.\\
        `Both, mandatory and non-mandatory fields are stored as object properties.`
        """
        io_metadata.check_tsdf_mandatory_fields(dictionary)
        for key, value in dictionary.items():
            setattr(self, key, value)