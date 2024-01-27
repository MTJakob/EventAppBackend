from marshmallow import Schema, fields


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
    StartDateTime = fields.DateTime('%Y-%m-%dT%H:%M:%S', required=True)
    EndDateTime = fields.DateTime('%Y-%m-%dT%H:%M:%S', required=True)
    Capacity = fields.Integer()


class EventDeleteSchema(Schema):
    IDEvent = fields.Integer(required=True)
