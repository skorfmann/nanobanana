from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("nanobanana")
except PackageNotFoundError:
    __version__ = "dev"
