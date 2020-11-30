
from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.instructions import Instruction
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from schemas.instruction import InstructionSchema



instruction_schema = InstructionSchema()
instruction_list_schema = InstructionSchema(many=True)

# Muista muuttaa instruction -> space
class InstructionListResource(Resource):

    def get(self):

        instructions = Instruction.get_all_published()

        return instruction_list_schema.dump(instructions).data, HTTPStatus.OK

    @jwt_required
    def post(self):

        json_data = request.get_json()
        current_user = get_jwt_identity()
        data, errors = instruction_schema.load(data=json_data)

        if errors:
            return {'message': "Validation errors", 'errors': errors}, HTTPStatus.BAD_REQUEST
        instruction = Instruction(**data)
        instruction.user_id = current_user
        instruction.save()

        return instruction_schema.dump(instruction).data, HTTPStatus.CREATED

        