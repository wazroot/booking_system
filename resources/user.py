from flask import request, url_for
from flask_restful import Resource
from http import HTTPStatus
from utils import hash_password, generate_token, verify_token
from models.user import User
from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required
from schemas.user import UserSchema
from http import HTTPStatus
from webargs import fields
from webargs.flaskparser import use_kwargs
from models.space import Space
from schemas.validations import SpaceSchema
from schemas.user import UserSchema
from mailgun import MailgunApi

space_list_schema = SpaceSchema(many=True)
user_schema = UserSchema()
user_public_schema = UserSchema(exclude=('email',))
mailgun = MailgunApi(domain='sandboxe6b1c63a9c6c44a39c6525059bd73550.mailgun.org',
                     api_key='eee238a177c8cf694348fec9b10efbfd-95f6ca46-63e18c82')


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
        token = generate_token(user.email, salt='activate')

        subject = 'Please confirm your registration.'

        link = url_for('useractivateresource', token=token, _external=True)

        text = 'Hi, Thanks for using our booking system! Please confirm your registration by clicking on the link: {}'.format(
            link)

        mailgun.send_email(to=user.email, subject=subject, text=text)
        return user_schema.dump(user).data, HTTPStatus.CREATED


class UserActivateResource(Resource):

    def get(self, token):

        email = verify_token(token, salt='activate')

        if email is False:
            return {'message': 'Invalid token or token expired'}, HTTPStatus.BAD_REQUEST

        user = User.get_by_email(email=email)

        if not user:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        if user.is_active is True:
            return {'message': 'The user account is already activated'}, HTTPStatus.BAD_REQUEST

        user.is_active = True

        user.save()

        return {}, HTTPStatus.NO_CONTENT
