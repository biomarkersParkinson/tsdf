"""
More convenient interface around TSDF files and datatypes.
"""

from datetime import datetime
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from .tsdfmetadata import TSDFMetadata
from .read_tsdf import load_metadata_from_path
from .read_binary import _load_binary_file
from .write_tsdf import write_metadata
from .write_binary import _get_metadata_from_ndarray


class ChannelMetadata:
    """
    Metadata for a single channel.
    """
    unit: str
    """The unit used for this channel."""

    def __init__(self, unit) -> None:
        self.unit = unit

class ChannelGroup:
    """
    A `ChannelGroup` is a group of channels that share the same data type, and that are stored together in a single data file.
    """

    channels: List[str]
    """Names of the channels in this group."""

    name: Optional[str]
    """Name of this channel group."""

    def __init__(self, channels: List[str], name: Optional[str] = None) -> None:
        self.channels = channels
        self.name = name


class RecordingMetadata:
    """
    Metadata for the recording in a tsdf file.

    In contrast to `tsdfmetadata.TSDFMetadata` this class only stores user-relevant attributes, and not the details of how the data is stored into a file.
    """

    study_id: str
    """Study ID."""
    
    subject_id: str
    """Subject ID."""
    
    device_id: str
    """Device ID."""
    
    start: datetime
    """Start time of the recording."""
    
    end: datetime
    """End time of the recording."""

    channel_metadata: Dict[str, ChannelMetadata]
    """Units and other metadata of the channels."""

    channel_groups: List[ChannelGroup]
    """Groups of channels that all have the same type, and are stored in a single data file."""

    @property
    def channels(self) -> List[str]:
        """Names of all channels"""
        return [channel for group in self.channel_groups for channel in group.channels]

    def __init__(self, study_id, subject_id, device_id, start, end, channel_metadata={}, channel_groups=[]) -> None:
        self.study_id = study_id
        self.subject_id = subject_id
        self.device_id = device_id
        self.start = start
        self.end = end
        self.channel_metadata = channel_metadata
        self.channel_groups = channel_groups

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary of recording related TSDF metadata attributes"""
        return {
            "study_id": self.study_id,
            "subject_id": self.subject_id,
            "device_id": self.device_id,
            "start_iso8601": self.start.isoformat(),
            "end_iso8601": self.end.isoformat(),
        }
        pass


class DataFile:
    """
    A data file that stores one or more channels from a TSDFRecording.
    """
    path: Path
    """Absolute path of this data file."""
    channels: List[str]
    """List of channels in this file."""


class BinaryDataFile(DataFile):
    """
    A binary data file that stores one or more channels from a TSDFRecording
    """
    data_type: str
    bits: int
    endianness: str
    rows: int

    def __init__(self, path: Path, channels: List[str], data_type: str, bits: int, endianness: str, rows: int):
        self.path = path
        self.channels = channels
        self.data_type = data_type
        self.bits = bits
        self.endianness = endianness
        self.rows = rows

    def to_dict(self) -> Dict[str, Any]:
        """Return a dictionary of file related TSDF metadata attributes"""
        return {
            "file_name": self.path.name,
            "channels": self.channels,
            "data_type": self.data_type,
            "bits": self.bits,
            "endianness": self.endianness,
            "rows": self.rows,
        }

    def read_numpy(self, start_row=0, end_row=-1) -> np.ndarray:
        """Read the file into a numpy array"""
        return _load_binary_file(
            str(self.path),
            self.data_type,
            self.bits,
            self.endianness,
            self.rows,
            len(self.channels),
            start_row,
            end_row,
        )


class TSDFRecording:
    """
    A single recording from a TSDF file.
    """

    meta: RecordingMetadata
    """Metadata for this recording."""

    _files: List[BinaryDataFile]
    """Files used to store this recording."""

    def __init__(self, meta: RecordingMetadata, files: List[BinaryDataFile]):
        self.meta = meta
        self._files = files
        assert [g.channels for g in meta.channel_groups] == [file.channels for file in files]

    @property
    def channels(self) -> List[str]:
        """Names of all channels in this recording."""
        return [channel for file in self._files for channel in file.channels]

    @property
    def subject_id(self) -> str:
        return self.meta.subject_id

    @property
    def study_id(self) -> str:
        return self.meta.study_id

    @property
    def device_id(self) -> str:
        return self.meta.device_id

    @property
    def start(self) -> datetime:
        return self.meta.start

    @property
    def end(self) -> datetime:
        return self.meta.end

    @property
    def channel_groups(self) -> List[ChannelGroup]:
        return self.meta.channel_groups

    def read_numpy(self, channels: List[str] | ChannelGroup) -> np.ndarray:
        """
        Read the channels with the given names into a numpy array.
        The channels must belong to the same channel group.

        :param channels: Names of the channels to read.
        """
        if isinstance(channels, ChannelGroup):
            channels = channels.channels
        # Find the file containing these channels
        for file in self._files:
            if channels[0] in file.channels:
                assert channels == file.channels, "Channels must match exactly with the channels in one of the data files."
                data = file.read_numpy()
                return data
        raise Exception(f"The requested channels are not found in any of the recording's files: {channels}")

    def read_dataframe(self, channels: Optional[List[str] | ChannelGroup] = None) -> pd.DataFrame:
        """
        Read the given channels into a pandas data frame.

        :param channels: Names of the channels to read. If None, then all channels are read.
        """
        if isinstance(channels, ChannelGroup):
            channels = channels.channels
        data_frames = []
        for file in self._files:
            # Do we need to load this file?
            need_to_load = channels is None or len(set(channels) & set(file.channels)) > 0
            if need_to_load:
                df = pd.DataFrame(file.read_numpy(), columns=file.channels)
                data_frames.append(df)
        df = pd.concat(data_frames, axis=1)
        if channels is not None:
            df = df[channels]
        set_metadata(df, self.meta)
        return df


# Store metadata in dataframe attributes

def get_metadata(df: pd.DataFrame) -> RecordingMetadata:
    """
    Get the metadata associated with a data frame.
    Fails if the data frame does not have metadata.
    """
    if 'tsdf_metadata' not in df.attrs:
        raise Exception('DataFrame does not have associated metadata. Use `set_metadata` to set it.')
    return df.attrs['tsdf_metadata']

def set_metadata(df: pd.DataFrame, metadata: RecordingMetadata) -> None:
    """
    Set the metadata associated with a data frame.
    """
    df.attrs['tsdf_metadata'] = metadata

pd.DataFrame.tsdf_metadata = property(get_metadata, set_metadata)
"""The tsdf_metadata property of a dataframe can be used instead of get_metadata/set_metadata."""


# Metadata conversion

def to_tsdf_metadata(recording: RecordingMetadata, file: BinaryDataFile) -> TSDFMetadata:
    """
    Combine metadata for a recording and a file into a TSDFMetadata object
    """
    dict = recording.to_dict() | file.to_dict()
    channel_metas = [recording.channel_metadata[c] for c in file.channels]
    dict['units'] = [c.unit for c in channel_metas]
    #if any(c.scale_factor is not None for c in channel_metas):
    #    dict['scale_factor'] = [(c.scale_factor if c.scale_factor is not None else 1.0) for c in channel_metas]
    dict['metadata_version'] = '0.1'
    return TSDFMetadata(dict, dir_path=str(file.path.parent))

def same_recording(meta1: TSDFMetadata, meta2: TSDFMetadata) -> bool:
    """
    Are two metadatas from the same recording?
    """
    return \
        meta1.study_id == meta2.study_id and \
        meta1.subject_id == meta2.subject_id and \
        meta1.device_id == meta2.device_id and \
        meta1.start_iso8601 == meta2.start_iso8601 and \
        meta1.end_iso8601 == meta2.end_iso8601 and \
        meta1.rows == meta2.rows

def channel_group_name(file_name: str) -> Optional[str]:
    """
    Come up with a channel group name based on a file name.

    For "path/file-with-suffix.bin" returns "suffix"
    """
    match = re.search(r"[-_.]([^-_./]+)[.][^./]+$", file_name)
    if match:
        return match.group(1)
    else:
        return None


def from_tsdf_metadata(meta: TSDFMetadata) -> Tuple[RecordingMetadata, BinaryDataFile]:
    """
    Split TSDF metadata into recording metadata and file metadata
    """
    channel_group = ChannelGroup(meta.channels, channel_group_name(meta.file_name))
    channel_metadata = {channel: ChannelMetadata(unit=unit) for channel, unit in zip(meta.channels, meta.units)}
    recording_meta = RecordingMetadata(
        study_id=meta.study_id,
        subject_id=meta.subject_id,
        device_id=meta.device_id,
        start=meta.get_start_datetime(),
        end=meta.get_end_datetime(),
        channel_metadata=channel_metadata,
        channel_groups=[channel_group])
    file_meta = BinaryDataFile(
        path=Path(meta.file_dir_path, meta.file_name),
        channels=meta.channels,
        data_type=meta.data_type,
        bits=meta.bits,
        endianness=meta.endianness,
        rows=meta.rows,
    )
    return recording_meta, file_meta

def metadata_to_recordings(metas: List[TSDFMetadata]) -> List[TSDFRecording]:
    out = []
    processed = [False for _ in metas]
    for i in range(len(metas)):
        if not processed[i]:
            # Split metadata
            combined_meta, file = from_tsdf_metadata(metas[i])
            files = [file]
            processed[i] = True
            # Find metas with the same recording
            for j in range(i+1, len(metas)):
                if not processed[j] and same_recording(metas[i], metas[j]):
                    # Combine metadata
                    meta, file = from_tsdf_metadata(metas[j])
                    combined_meta.channel_groups.extend(meta.channel_groups)
                    combined_meta.channel_metadata.update(meta.channel_metadata)
                    files.append(file)
                    processed[j] = True # Set to None to indicate we processed this file
            recording = TSDFRecording(combined_meta, files)
            out.append(recording)
    return out


# Reading


def read_multi_recording_metadata(metadata_path: Path | str) -> List[TSDFRecording]:
    """
    Load a tsdf metadata file that contains one or more TSDF recordings.

    :param metadata_path: Full path to the metadata file.
    """
    metas = load_metadata_from_path(Path(metadata_path))
    return metadata_to_recordings(list(metas.values()))

def read_single_recording_metadata(metadata_path: Path | str) -> TSDFRecording:
    """
    Load a tsdf metadata file that contains a single TSDF recording.

    Raises an Exception if there is not exactly one recording in the metadata file.

    :param metadata_path: Full path to the metadata file.
    """
    recordings = read_multi_recording_metadata(metadata_path)
    if len(recordings) == 1:
        return recordings[0]
    else:
        raise Exception(f"File does not contain a single recording, found {len(recordings)} recordings in metadata")

def read_single_recording_dataframe(metadata_path: Path | str, channels: Optional[List[str] | ChannelGroup] = None) -> pd.DataFrame:
    """
    Load a dataframe from a tsdf metadata file that contains a single TSDF recording.

    Raises an Exception if there is not exactly one recording in the metadata file.

    :param metadata_path: Full path to the metadata file.
    :param channels: Names of the channels to read. If None, then all channels are read.
    """
    return read_single_recording_metadata(metadata_path).read_dataframe(channels)

# alias
read_recording = read_single_recording_metadata
read_dataframe = read_single_recording_dataframe


# Writing


def write_numpy_without_metadata(metadata_path: Path | str, suffix: str, data: np.ndarray, channels: List[str] | ChannelGroup) -> BinaryDataFile:
    """
    Write a numpy array to a binary data data file.
    If the metadata path is "dir/file.json", then the data will be stored in "dir/file.{suffix}.bin".

    :param metadata_path: Full path to the metadata file.
    :param suffix: Suffix to use for this data file.
    :param data: Data to store.
    :param channels: Names of the channels in the array.

    :return: DataFile object that contains data about the written file.
    """
    if isinstance(metadata_path, str):
        metadata_path = Path(metadata_path)
    if isinstance(channels, ChannelGroup):
        channels = channels.channels
    assert \
        len(data.shape) == 1 and len(channels) == 1 or \
        len(data.shape) == 2 and len(channels) == data.shape[1], \
        "The number of columns in data should match the number of channels"
    path = metadata_path.with_suffix('.' + suffix + '.bin')
    data.tofile(path)
    meta = BinaryDataFile(path, channels, **_get_metadata_from_ndarray(data))
    return meta

def write_dataframe_without_metadata(metadata_path: Path | str, df: pd.DataFrame, channel_groups: List[ChannelGroup]) -> List[BinaryDataFile]:
    """
    Write a pandas dataframe to data files.
    Each channel group is written to a separate file.
    If the metadata path is "dir/file.json", then the data will be stored in files "dir/file.{suffix}.bin".

    :param metadata_path: Full path to the metadata file.
    :param df: dataframe to write.
    :param suffix: Suffix to use for this data file.
    :param channel_groups: Channel groups to write to files. This should match the columns in the DataFrame.

    :return: A list of DataFile objects that contains data about the written files.
    """
    # Check that all channels are in a channel group
    channels_in_channel_groups = sorted([channel for g in channel_groups for channel in g.channels])
    channels_in_dataframe = sorted(list(df.columns))
    assert channels_in_channel_groups == channels_in_dataframe, "The channel groups do not match the columns in the DataFrame"
    # Write all channel groups
    out = []
    for i, channel_group in enumerate(channel_groups):
        data = df[channel_group.channels].to_numpy()
        suffix = channel_group.name if channel_group.name is not None else str(i)
        file = write_numpy_without_metadata(metadata_path, suffix, data, channel_group)
        out.append(file)
    return out

def write_recording_metadata(metadata_path: Path | str, recordings: TSDFRecording | List[TSDFRecording]) -> None:
    """"
    Write metadata for one or more TSDFRecordings.

    This function assumes that the data for the recordings is already written to files.

    :param metadata_path: Full path to the metadata file.
    """
    if not isinstance(recordings, List):
        recordings = [recordings]
    # Gather metadata for all files
    meta = [to_tsdf_metadata(recording.meta, file) for recording in recordings for file in recording._files]
    write_metadata(meta, str(metadata_path))

def write_dataframe(path, df: pd.DataFrame) -> TSDFRecording:
    """
    Write a dataframe to a tsdf metadata file and associated data files.

    :param path: Path to the metadata file that will be written.
    :param df: DataFrame to write to the file. This dataframe should have associated metadata, set with `set_metadata`.

    :return: TSDFRecording object for the saved file.
    """
    meta = get_metadata(df)
    files = write_dataframe_without_metadata(path, df, meta.channel_groups)
    recording = TSDFRecording(meta, files)
    write_recording_metadata(path, recording)
    return recording
