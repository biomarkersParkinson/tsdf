import sys
import numpy as np


_map_from_numpy_types = {
    "i": "int",
    "f": "float",
    # etc
}
""" Mapping of NumPy data types to their TSDF metadata annotations. """


def data_type_numpy_to_tsdf(data: np.ndarray):
    """Compute the TSDF metadata 'data_type' value, based on the NumPy data."""
    return _map_from_numpy_types[data.dtype.kind]


_map_to_numpy_types = {
    "int": "i",
    "float": "f",
    # etc
}
""" Mapping of data types that are supported by TSDF to 
    their NumPy representation used for parsing. """


def data_type_tsdf_to_numpy(data_type: str) -> str:
    """
    Compute the the NumPy data type, based on the TSDF metadata 'data_type' value.

    :param data_type: TSDF metadata 'data_type' value.

    :return: NumPy data type (as a char).
    """
    return _map_to_numpy_types[data_type]


def bits_numpy_to_tsdf(data: np.ndarray) -> int:
    """
    Compute TSDF metadata 'n_bits' value, based on the NumPy data.

    :param data: NumPy data.

    :return: TSDF metadata 'n_bits' value.
    """
    return data.dtype.itemsize * 8


def bytes_tsdf_to_numpy(n_bits: int):
    """
    Compute the the NumPy byte number, based on the TSDF metadata 'n_bits' value.

    :param n_bits: TSDF metadata 'n_bits' value.

    :return: NumPy byte number.
    """
    return str(n_bits // 8)


_map_from_numpy_endianness = {
    "<": "little",
    ">": "big",
    "=": sys.byteorder,
}
""" Supported endianness values. """


def endianness_numpy_to_tsdf(data: np.ndarray) -> str:
    """
    Compute TSDF metadata 'data_type' value, based on the NumPy data.

    :param data: NumPy data.

    :return: TSDF metadata 'data_type' value (as a string).
    """
    return _map_from_numpy_endianness[data.dtype.byteorder]


_map_to_numpy_endianness = {
    "little": "<",
    "big": ">",
}
""" Supported endianness values. """


def endianness_tsdf_to_numpy(endianness: str) -> str:
    """
    Compute TSDF metadata 'data_type' value, based on the NumPy data.

    :param endianness: TSDF metadata 'data_type' value.

    :return: NumPy data type (as a char)."""
    return _map_to_numpy_endianness[endianness]


def rows_numpy_to_tsdf(data: np.ndarray) -> int:
    """
    Compute TSDF metadata 'rows' value, based on the NumPy data.

    :param data: NumPy data.

    :return: TSDF metadata 'rows' value.
    """
    return data.shape[0]
