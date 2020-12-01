
from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.space import Space
from models.reservation import Reservation
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional

from schemas.validations import InstructionSchema
# Muista muuttaa importit!!!


space_schema = InstructionSchema()
space_list_schema = InstructionSchema(many=True)

# Muista muuttaa instruction -> space
class SpaceListResource(Resource):

    #get all spaces.
    def get(self):

        space = Space.get_by_id()

        return space_list_schema.dump(space).data, HTTPStatus.OK

    @jwt_required
    def post(self):

        json_data = request.get_json()
        #current_user = get_jwt_identity()
        data, errors = space_schema.load(data=json_data)

        if errors:
            return {'message': "Validation errors", 'errors': errors}, HTTPStatus.BAD_REQUEST
        space = Space(**data)
        #instruction.user_id = current_user
        space.save()

        return space_schema.dump(space).data, HTTPStatus.CREATED

# Muista muuttaa instruction -> space
class SpaceResource(Resource):

    @jwt_optional
    def get(self, space_id):#get a spesific space

        space = Space.get_by_id(space_id)


        if space is None:
            return {'message': 'instruction not found'}, HTTPStatus.NOT_FOUND

        # current_user = get_jwt_identity()

        # if space.is_publish == False and space.user_id != current_user:
        #     return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return space_schema.dump(space).data, HTTPStatus.OK


    @jwt_required
    def put(self, space_id):#update a spesific spaces atrributes

        json_data = request.get_json()

        space = Space.get_by_id(space_id)


        if space is None:
            return {'message': 'instruction not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != space.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN


        space.id = json_data['id']
        space.name = json_data['name']
        space.capacity = json_data['capasity']

        space.save()

        return space.data(), HTTPStatus.OK

    @jwt_required
    def delete(self, space_id):#delete a spesific space

        space = Space.get_by_id(space_id)

        if space is None:
            return {'message': 'instruction not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != space.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN


        space.delete()

        return {}, HTTPStatus.NO_CONTENT

    # @jwt_required
    # def patch(self, instruction_id):
    #     json_data = request.get_json()
    #
    #     data, errors = instruction_schema.load(data=json_data, partial=('name',))
    #
    #     if errors:
    #         return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST
    #
    #     instruction = Instruction.get_by_id(instruction_id=instruction_id)
    #
    #     if instruction is None:
    #         return {'message': 'Instruction not found'}, HTTPStatus.NOT_FOUND
    #
    #     current_user = get_jwt_identity()
    #
    #     if current_user != instruction.user_id:
    #         return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
    #
    #     instruction.name = data.get('name') or instruction.name
    #     instruction.description = data.get('description') or instruction.description
    #     instruction.steps = data.get('steps') or instruction.steps
    #     instruction.tools = data.get('tools') or instruction.tools
    #     instruction.cost = data.get('cost') or instruction.cost
    #     instruction.duration = data.get('duration') or instruction.duration
    #     instruction.save()
    #     return instruction_schema.dump(instruction).data, HTTPStatus.OK

# Muista muuttaa instruction -> space
class SpacePublic(Resource):#Ei tätä taideta tarvita? listaa julkaistut tilat?
    @jwt_required
    def put(self, instruction_id):
        instruction = Instruction.get_by_id(instruction_id=instruction_id)

        if instruction is None:
            return {'message': 'instruction not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != instruction.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        instruction.is_publish = True
        instruction.save()

        return {}, HTTPStatus.NO_CONTENT

    @jwt_required
    def delete(self, instruction_id):
        instruction = Instruction.get_by_id(instruction_id=instruction_id)

        if instruction is None:
            return {'message': 'instruction not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != instruction.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        instruction.is_publish = False
        instruction.save()

        return {}, HTTPStatus.NO_CONTENT
