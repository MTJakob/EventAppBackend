from marshmallow import Schema, fields
from schemas.PlainSchemas import PlainUserSchema, PlainCategorySchema, PlainEventSchema, PlainAddressSchema


class EventGetSchema(Schema):
    Name = fields.Str()
    SearchWord = fields.Str()


class LoginSchema(Schema):
    Email = fields.Str(required=True)
    Password = fields.Str(required=True, load_only=True)


class RegisterSchema(Schema):
    Email = fields.Email(required=True)
    Name = fields.Str(required=True)
    Surname = fields.Str(required=True)
    DateOfBirth = fields.DateTime('%Y-%m-%d', required=True)
    Password = fields.Str(required=True, load_only=True)


class EventPostSchema(PlainEventSchema):
    eventCategory = fields.Nested(PlainCategorySchema(only=("Name",)))
    eventAddress = fields.Nested(PlainAddressSchema(exclude=("IDAddress", "Name")))


class EventPutSchema(PlainEventSchema):
    eventCategory = fields.Nested(PlainCategorySchema(only=("Name",)))
    eventAddress = fields.Nested(PlainAddressSchema(exclude=("IDAddress", "Name")))


class EventDeleteSchema(Schema):
    IDEvent = fields.Integer(required=True)


class EventParticipantDeleteSchema(Schema):
    IDEvent = fields.Integer(required=True)