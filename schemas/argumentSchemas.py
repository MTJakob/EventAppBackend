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


class EventPostSchema(Schema):
    Name = fields.Str(required=True)
    Price = fields.Float()
    StartDateTime = fields.DateTime('%Y-%m-%dT%H:%M:%S')
    EndDateTime = fields.DateTime('%Y-%m-%dT%H:%M:%S')
    Capacity = fields.Integer()
    eventCategory = fields.Nested(PlainCategorySchema(only=("Name",)), dump_only=True)
    eventAddress = fields.Nested(PlainAddressSchema(exclude=("IDAddress", "Name")), dump_only=True)


class EventDeleteSchema(Schema):
    IDEvent = fields.Integer(required=True)


class EventGetSchema(PlainEventSchema):
    eventOrganiser = fields.Nested(PlainUserSchema(exclude=("Email", "DateOfBirth",)), dump_only=True)
    eventCategory = fields.Nested(PlainCategorySchema(only=("Name",)), dump_only=True)
    eventAddress = fields.Nested(PlainAddressSchema(exclude=("IDAddress", "Name")), dump_only=True)
