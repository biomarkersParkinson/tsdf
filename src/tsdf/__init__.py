# read version from installed package
from importlib.metadata import version
from tsdf.tsdf_metadata import TSDFMetadata
__version__ = version("tsdf")
