import graphene
import message_app.schema


class Queries(
    message_app.schema.Query,
    graphene.ObjectType
):
    dummy = graphene.String()


schema = graphene.Schema(query=Queries)
