from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError
from schemas.user import UserSchema
from models.reservation import Reservation

class SpaceSchema(Schema):
    author = fields.Nested(UserSchema, attribute='user', dump_only=True, only=['id', 'username'])

    def validate_capacity(n):
        if n < 2:
            raise ValidationError('Capacity must be greater than 1.')
        if n > 24:
            raise ValidationError('Capacity must not be greater than 24.')

    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=100)])
    capacity = fields.Integer(required=True, validate=validate_capacity)
    created_at = fields.DateTime(dump_only=True)


    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {'data': data}
        return data


class ReservationSchema(Schema):

    id = fields.Integer(dump_only=True)
    time = fields.String(required=True)
    space_id = fields.Integer(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


