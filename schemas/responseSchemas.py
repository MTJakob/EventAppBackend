from marshmallow import fields
from schemas.PlainSchemas import PlainEventSchema, PlainUserSchema, PlainCategorySchema, PlainAddressSchema


class EventGetSchema(PlainEventSchema):
    eventUser = fields.Nested(PlainUserSchema(exclude=("Email", "DateOfBirth",)), dump_only=True)
    eventCategory = fields.Nested(PlainCategorySchema(only=("Name",)), dump_only=True)
    eventAddress = fields.Nested(PlainAddressSchema(exclude=("IDAddress", "Name")), dump_only=True)

