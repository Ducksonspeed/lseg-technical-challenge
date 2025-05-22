import pytest
import logging
from io import StringIO

import sys
import os

# Include parent directory to python import path.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def log_capture():
    output = StringIO()

    handler = logging.StreamHandler(output)
    handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))

    logger = logging.getLogger()
    logger.handlers = [handler]
    logger.setLevel(logging.INFO)  # Capture INFO and higher by default

    return output  # The test can access captured logs via getvalue()