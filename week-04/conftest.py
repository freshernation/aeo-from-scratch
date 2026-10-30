"""Week 4: puts rewrite_checks.py on the path and gives the tests the snapshot web."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

from rewrite_checks import SNAPSHOT  # noqa: E402

from aeolab import web2  # noqa: E402


@pytest.fixture
def snapshot_web():
    return web2(SNAPSHOT)
