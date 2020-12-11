from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError
from schemas.user import UserSchema
from flask_jwt_extended import get_jwt_identity


class SpaceSchema(Schema):
    author = fields.Nested(UserSchema, attribute='user', dump_only=True, only=['id', 'username'])

    #@validates('capacity')
    #def validate_capacity(n):
    #    if n < 2:
    #        raise ValidationError('Capacity must be greater than 1.')
    #    if n > 24:
    #        raise ValidationError('Capacity must not be greater than 24.')

    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=100)])
    capacity = fields.Integer(required=True)
    created_at = fields.DateTime(dump_only=True)

    '''
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
        '''

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {'data': data}
        return data


class ReservationSchema(Schema):
    id = fields.Integer(dump_only=True)
    time = fields.Date(required=True)
    user_id = fields.Integer(required=True)
    space_id = fields.Integer(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    '''@validates('time')
    def validate_time(self,f):
        if f == time:
            raise ValidationError('already taken')'''
