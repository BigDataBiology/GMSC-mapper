import shutil
import pytest

def requires_binary(name):
    return pytest.mark.skipif(
        shutil.which(name) is None,
        reason=f"{name} not found in PATH"
    )
