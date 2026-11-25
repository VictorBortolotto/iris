import pytest

from Main import app

@pytest.fixture
def app_context():
  with app.app_context():
    yield