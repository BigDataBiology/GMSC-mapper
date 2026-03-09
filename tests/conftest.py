import shutil
import pytest

from gmsc_mapper.gmsc_mapper_version import __version__

def requires_binary(name):
    return pytest.mark.skipif(
        shutil.which(name) is None,
        reason=f"{name} not found in PATH"
    )


VERSION_COMMENT = f"# GMSC-mapper version {__version__}"


def read_text_without_version_comment(fname):
    with open(fname, "rt") as f:
        lines = f.readlines()
    if lines and lines[0].rstrip("\n") == VERSION_COMMENT:
        lines = lines[1:]
    return "".join(lines)


def has_version_comment(fname):
    with open(fname, "rt") as f:
        return f.readline().rstrip("\n") == VERSION_COMMENT
