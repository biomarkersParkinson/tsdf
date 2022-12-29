from dataclasses import dataclass
from typing import List

@dataclass
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
    properties: dict
    """ Additional (non-obligatory) properties provided by the methadata. """

