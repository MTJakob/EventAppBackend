from marshmallow import Schema, fields


class EventSchema(Schema):
    name = fields.Str(required=True)
