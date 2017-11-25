import graphene
from graphene_django.types import DjangoObjectType
from graphql_relay.node.node import from_global_id
from . import models


class MessageType(DjangoObjectType):
    class Meta:
        model = models.Message
        interfaces = (graphene.Node, )


class Query(graphene.ObjectType):
    message = graphene.Field(MessageType, id=graphene.ID())

    def resolve_message(self, args):
        rid = from_global_id(args.get('id'))
        # rid is a tuple: ('MessageType', '1')
        return models.Message.objects.get(pk=rid[1])


    all_messages = graphene.List(MessageType)

    def resolve_all_messages(self, args):
        return models.Message.objects.all()
