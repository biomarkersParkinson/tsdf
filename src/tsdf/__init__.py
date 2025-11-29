# read version from installed package
from importlib.metadata import version

__version__ = version("tsdf")

from .read_tsdf import (
    load_metadata_file,
    load_metadata_from_path,
    load_metadatas_from_dir,
    load_metadata_string,
    load_metadata_legacy_file,
)
from .write_tsdf import (
    write_metadata,
)

from .write_binary import (
    write_binary_file,
    write_dataframe_to_binaries,
)
from .read_binary import (
    load_ndarray_from_binary,
    load_dataframe_from_binaries,
)

from .tsdfmetadata import TSDFMetadata

from .time_series import (
    ChannelMetadata,
    ChannelGroup,
    TimeSeriesMetadata,
    TSDFTimeSeries,
    read_multi_time_series_metadata,
    read_time_series,
    read_dataframe,
    write_dataframe,
)

__all__ = [
    "load_metadata_file",
    "load_metadata_from_path",
    "load_metadatas_from_dir",
    "load_metadata_string",
    "load_metadata_legacy_file",
    "write_metadata",
    "write_binary_file",
    "write_dataframe_to_binaries",
    "load_ndarray_from_binary",
    "load_dataframe_from_binaries",
    "TSDFMetadata",
    "ChannelMetadata",
    "ChannelGroup",
    "TimeSeriesMetadata",
    "TSDFTimeSeries",
    "read_multi_time_series_metadata",
    "read_time_series",
    "read_dataframe",
    "write_dataframe",
]
