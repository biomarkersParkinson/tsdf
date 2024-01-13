import numpy as np
from pathlib import Path
import tsdf


def load_single_bin_file(data_dir: Path, name: str) -> np.ndarray:
    """
    Load a single binary file from the given directory path and file name.

    :param dir_path: The directory path where the binary file is located.
    :param file_name: The name of the binary file without the extension.

    :returns: The binary data as a numpy array.
    """
    metadata = tsdf.load_metadata_from_path(data_dir / (name + "_meta.json"))
    data = tsdf.load_ndarray_from_binary(metadata[name + ".bin"])
    return data
