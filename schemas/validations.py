from marshmallow import Schema, fields, post_dump, validate, validates,ValidationError
from schemas.user import UserSchema
from flask_jwt_extended import get_jwt_identity

class SpaceSchema(Schema):

    author = fields.Nested(UserSchema, attribute='user', dump_only=True, only=['id', 'username'])

    class Meta:
        ordered = True
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=100)])
    capacity = fields.Integer(dump_only=True)
    #is_publish = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    def validate_steps(n):
        if n < 1:
            raise ValidationError('Number of steps must be greater than 0.')
        if n > 50:
            raise ValidationError('Number of steps must not be greater than 50.')

       
    steps = fields.Integer(validate=validate_steps)

    def validate_cost(n):
        if n < 1:
            raise ValidationError('cost must be greater than 0.')
        if n > 100:
            raise ValidationError('cost must not be greater than 100.')
    cost=fields.Integer(validate=validate_cost)
    duration = fields.Integer()

    @validates('duration')
    def validate_duration(self, value):
        if value < 1:
            raise ValidationError('Duration time must be greater than 0.')

        if value > 300:
            raise ValidationError('Duration time must not be greater than 300.')

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {'data': data}
        return data


class ReservationSchema(Schema):

    id = fields.Integer(dump_only=True)
    time = fields.DateTime(dump_only=True)
    user_id = fields.String(dump_only=True)
    space_id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)