import graphene
from graphene_django.types import DjangoObjectType
from graphql_relay.node.node import from_global_id
from graphene_django.filter.fields import DjangoFilterConnectionField
from . import models
import json

class MessageType(DjangoObjectType):
    class Meta:
        model = models.Message
        filter_fields = {'message': ['icontains']}
        interfaces = (graphene.Node, )

class UserInput(graphene.InputObjectType):
    id = graphene.ID(required=False)


class Query(graphene.ObjectType):
    id = graphene.Field(MessageType, input=UserInput())

    def resolve_message(self, info, input):
        id = input.get('id')

        # rid = from_global_id(args.get('id'))
        # rid is a tuple: ('MessageType', '1')
        # return models.Message.objects.get(pk=rid[1])
        return Message.objects.get(pk=id)

    all_messages = DjangoFilterConnectionField(MessageType)

    def resolve_all_messages(self, *args):
        return models.Message.objects.all()


class CreateMessageMutation(graphene.Mutation):
    class Arguments:
        message = graphene.String()

    status = graphene.Int()
    formErrors = graphene.String()
    message = graphene.Field(MessageType)

    @staticmethod
    def mutate(root, req, args={}):
        if not req.user.is_authenticated:
            return CreateMessageMutation(status=403)
        message = args.get('message', '').strip()
        # Typically use Django forms to validate the input
        if not message:
            return CreateMessageMutation(
                status=400,
                formErrors=json.dumps(
                    {'message': ['Please enter a message.']}))
        obj = models.Message.objects.create(
            user=req.user, message=message
        )
        return CreateMessageMutation(status=200, message=obj)


class Mutation(object):
    create_message = CreateMessageMutation.Field()
