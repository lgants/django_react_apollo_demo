import pytest
from mixer.backend.django import mixer

# Need to enable writing to the DB in tests
pytestmark = pytest.mark.django_db


def test_message():
    obj = mixer.blend('message_app.Message')
    assert obj.pk > 0
