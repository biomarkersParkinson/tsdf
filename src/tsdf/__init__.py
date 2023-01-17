# read version from installed package
from importlib.metadata import version
__version__ = version("tsdf")
import tsdf.io
import tsdf.io_metadata
