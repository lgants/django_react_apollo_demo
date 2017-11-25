import pytest
from mixer.backend.django import mixer
from .. import schema
from IPython import embed
from graphql_relay.node.node import to_global_id

pytestmark = pytest.mark.django_db


def test_message_type():
    instance = schema.MessageType()
    assert instance

def test_resolve_message():
    # mixer.blend generates a model's instance and saves to db
    msg = mixer.blend('message_app.Message')
    q = schema.Query()
    id = to_global_id('MessageType', msg.pk)
    res = q.resolve_message({'id': id})
    assert res == msg, 'Should return the requested message'

def test_resolve_all_messages():
    mixer.blend('message_app.Message')
    mixer.blend('message_app.Message')
    q = schema.Query()
    res = q.resolve_all_messages(None)
    assert res.count() == 2, 'Should return all messages'
