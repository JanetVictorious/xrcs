import os
from unittest.mock import patch

import pytest


@pytest.fixture(scope='session', autouse=True)
def kivy_config():
    """Configure Kivy for headless testing."""
    os.environ['KIVY_NO_ARGS'] = '1'
    os.environ['KIVY_NO_CONSOLELOG'] = '1'
    os.environ['KIVY_GRAPHICS'] = 'mock'
    os.environ['KIVY_WINDOW'] = 'mock'

    # Patch Kivy's Window to avoid display initialization
    with patch('kivy.core.window.Window'):
        yield
