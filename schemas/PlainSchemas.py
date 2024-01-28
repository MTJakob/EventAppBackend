from marshmallow import Schema, fields


class PlainAddressSchema(Schema):
    IDAddress = fields.Integer()
    Name = fields.Str()
    Longitude = fields.Float()
    Latitude = fields.Float()


class PlainUserSchema(Schema):
    IDUser = fields.Integer()
    Email = fields.Email()
    Name = fields.Str()
    Surname = fields.Str()
    DateOfBirth = fields.DateTime('%Y-%m-%d')


class PlainCategorySchema(Schema):
    IDCategory = fields.Integer()
    Name = fields.Str()
    IDCategoryParent = fields.Integer()


class PlainEventSchema(Schema):
    IDEvent = fields.Integer()
    Name = fields.Str(required=True)
    Price = fields.Float()
    StartDateTime = fields.DateTime('%Y-%m-%dT%H:%M:%S')
    EndDateTime = fields.DateTime('%Y-%m-%dT%H:%M:%S')
    Capacity = fields.Integer()


class PlainEventParticipantSchema(Schema):
    IDUser = fields.Integer()
    IDEvent = fields.Integer()
    Review = fields.Integer()


class PlainRoleSchema(Schema):
    IDRole = fields.Integer()
    Name = fields.Str()
    LastUpdate = fields.DateTime('%Y-%m-%dT%H:%M:%S')
    CreatDate = fields.DateTime('%Y-%m-%dT%H:%M:%S')


class PlainPermissionSchema(Schema):
    IDPermission = fields.Integer()
    IDUser = fields.Integer()
    IDRole = fields.Integer()
    IDEvent = fields.Integer()
    LastUpdate = fields.DateTime('%Y-%m-%dT%H:%M:%S')
    CreatDate = fields.DateTime('%Y-%m-%dT%H:%M:%S')


class EventSchema(PlainEventSchema):
    IDOrganiser = fields.Integer()
    eventCategory = fields.Nested(PlainCategorySchema(only=("Name",)), dump_only=True)
    eventAddress = fields.Nested(PlainAddressSchema(), dump_only=True)
    #eventParticipantEventFrom = fields.List(fields.Nested(PlainEventParticipantSchema()), dump_only=True)
