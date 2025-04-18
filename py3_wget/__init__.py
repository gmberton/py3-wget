"""A tool to download files. It supports progress bar, cksum, timeout, retry failed download."""

from .__version__ import __version__
from .main import download_file
