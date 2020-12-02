
from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.space import Space
from models.reservation import Reservation
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from schemas.validations import SpaceSchema



space_schema = SpaceSchema()
space_list_schema = SpaceSchema(many=True)


class SpaceListResource(Resource):

    def get(self):

        space = Space.get_by_id()

        return space_list_schema.dump(space).data, HTTPStatus.OK

    @jwt_required
    def post(self):

        json_data = request.get_json()
        current_user = get_jwt_identity()
        
        data, errors = space_schema.load(data=json_data)

        if errors:
            return {'message': "Validation errors", 'errors': errors}, HTTPStatus.BAD_REQUEST
        space = Space(**data)
        space.user_id = current_user
        space.save()

        return space_schema.dump(space).data, HTTPStatus.CREATED


class SpaceResource(Resource):

    @jwt_optional
    def get(self, space_id):

        space = Space.get_by_id(space_id=space_id)

        if space is None:
            return {'message': 'space not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if space.is_publish == False and space.user_id != current_user:
        return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN                

        return space_schema.dump(space).data, HTTPStatus.OK


    @jwt_required
    def put(self, space_id):

        json_data = request.get_json()

        space = Space.get_by_id(space_id)


        if space is None:
            return {'message': 'space not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != space.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN


        space.id = json_data['id']
        space.name = json_data['name']
        space.capacity = json_data['capasity']

        space.save()

        return space.data(), HTTPStatus.OK

    @jwt_required
    def delete(self, space_id):

        space = Space.get_by_id(space_id)

        if space is None:
            return {'message': 'space not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != space.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN


        space.delete()

        return {}, HTTPStatus.NO_CONTENT

    @jwt_required
    def patch(self, space_id):
        json_data = request.get_json()

        data, errors = space_schema.load(data=json_data, partial=('name',))

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        space = Space.get_by_id(space_id=space_id)

        if space is None:
            return {'message': 'Space not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != space.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        space.name = data.get('name') or space.name
        space.description = data.get('description') or space.description
        space.steps = data.get('steps') or space.steps
        space.tools = data.get('tools') or space.tools
        space.cost = data.get('cost') or space.cost
        space.duration = data.get('duration') or space.duration
        space.save()
        return space_schema.dump(space).data, HTTPStatus.OK


class SpacePublic(Resource):#Ei tätä taideta tarvita? listaa julkaistut tilat?
    @jwt_required
    def put(self, space_id):
        space = Space.get_by_id(space_id=space_id)

        if space is None:
            return {'message': 'space not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != space.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        space.is_publish = True
        space.save()

        return {}, HTTPStatus.NO_CONTENT

    @jwt_required
    def delete(self, space_id):
        space = Space.get_by_id(space_id=space_id)

        if space is None:
            return {'message': 'space not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != space.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        space.is_publish = False
        space.save()

        return {}, HTTPStatus.NO_CONTENT
