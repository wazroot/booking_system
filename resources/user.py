from flask import request
from flask_restful import Resource
from http import HTTPStatus
from utils import hash_password
from models.user import User
from flask_jwt_extended import jwt_optional, get_jwt_identity
from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required
from schemas.user import UserSchema
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from http import HTTPStatus
from webargs import fields
from webargs.flaskparser import use_kwargs
from models.space import Space                      #Instructions muuttui -> Space
from schemas.validations import SpaceSchema
from schemas.user import UserSchema

                                                   #instructions_list_schema muuttui -> space_list_schema
space_list_schema = SpaceSchema(many=True)         #InstructionSchema muuttui -> SpaceSchema
user_schema = UserSchema()
user_public_schema = UserSchema(exclude=('email', ))

class UserSpaceListResource(Resource):
    @jwt_optional
    @use_kwargs({'visibility': fields.Str(missing='public')})
    def get(self, username, visibility):
        user = User.get_by_username(username=username)
        if user is None:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        if current_user == user.id and visibility in ['all', 'private']:
            pass
        else:
            visibility = 'public'
        space = Space.get_all_by_user(user_id=user.id,visibility=visibility)
        return space_list_schema.dump(space).data, HTTPStatus.OK

class MeResource(Resource):
    @jwt_required
    def get(self):
        user = User.get_by_id(id=get_jwt_identity())
        return user_schema.dump(user).data, HTTPStatus.OK

class UserResource(Resource):
    @jwt_optional
    def get(self, username):
        user = User.get_by_username(username=username)
        if user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        if current_user == user.id:
            data = user_schema.dump(user).data
        else:
            data = user_public_schema.dump(user).data
        return data, HTTPStatus.OK

class UserListResource(Resource):
    def post(self):
        json_data = request.get_json()
        data, errors = user_schema.load(data=json_data)
        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST
        if User.get_by_username(data.get('username')):
            return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST
        if User.get_by_email(data.get('email')):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST
        user = User(**data)
        user.save()
        return user_schema.dump(user).data, HTTPStatus.CREATED