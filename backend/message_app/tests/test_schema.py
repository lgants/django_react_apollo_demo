import pytest
from mixer.backend.django import mixer
from .. import schema
from IPython import embed

pytestmark = pytest.mark.django_db


def test_message_type():
    instance = schema.MessageType()
    assert instance

def test_resolve_all_messages():
    mixer.blend('message_app.Message')
    mixer.blend('message_app.Message')
    q = schema.Query()
    res = q.resolve_all_messages(None, None, None)
    assert res.count() == 2, 'Should return all messages'
