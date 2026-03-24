from importlib import metadata
from clickqt_utils.extensions import PathWithExtensions


__version__ = metadata.version(__package__)

__all__ = ["PathWithExtensions", "__version__"]
