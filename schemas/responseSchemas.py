from marshmallow import fields
from schemas.PlainSchemas import PlainEventSchema, PlainUserSchema, PlainCategorySchema, PlainAddressSchema,\
    PlainEventParticipantSchema


class EventGetSchema(PlainEventSchema):
    eventUser = fields.Nested(PlainUserSchema(exclude=("Email", "DateOfBirth",)), dump_only=True)
    eventCategory = fields.Nested(PlainCategorySchema(only=("Name",)), dump_only=True)
    eventAddress = fields.Nested(PlainAddressSchema(exclude=("IDAddress", "Name")), dump_only=True)
    # eventParticipantEventFrom = fields.Nested(PlainEventParticipantSchema(exclude=("Review",)), dump_only=True)
    # is_singed = fields.Method("is_signed_up_for_the_event", dump_only=True)
    # is_singed_lambda = fields.Function(lambda obj: not obj.eventParticipantEventFrom, dump_only=True)
    #
    # def is_signed_up_for_the_event(self, obj):
    #     if bool(obj.eventParticipantEventFrom):
    #         return True
    #     return False
