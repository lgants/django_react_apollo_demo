import graphene
import message_app.schema


class Mutations(
    message_app.schema.Mutation,
    graphene.ObjectType,
):
    pass

class Queries(
    message_app.schema.Query,
    graphene.ObjectType
):
    dummy = graphene.String()


schema = graphene.Schema(query=Queries, mutation=Mutations)
