import pytest
from mixer.backend.django import mixer
from .. import schema
from IPython import embed
from graphql_relay.node.node import to_global_id
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

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

def test_create_message_mutation():
    user = mixer.blend('auth.User')
    mut = schema.CreateMessageMutation()

    data = {'message': 'Test'}
    req = RequestFactory().get('/')
    req.user = AnonymousUser()
    res = mut.mutate(None, req, data)
    assert res.status == 403, 'Should return 403 if user is not logged in'

    req.user = user
    res = mut.mutate(None, req, {})
    assert res.status == 400, 'Should return 400 if there are form errors'
    assert 'message' in res.formErrors, (
        'Should have form error for message field')

    req.user = user
    res = mut.mutate(None, req, {'message': 'Test'})
    assert res.status == 200, 'Should return 400 if there are form errors'
    assert res.message.pk == 1, 'Should create new message'
