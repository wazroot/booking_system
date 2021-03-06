from models.reservation import Reservation
from schemas.validations import ReservationSchema
from flask import request
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional

'''This is our main interface. Here we CRUD a reservation, get reservations for a 
specific user and reservations for a specific space.'''

reservation_schema = ReservationSchema()
reservation_list_schema = ReservationSchema(many=True)


class ReservationListResource(Resource):

    def get(self):
        reservation = Reservation.get_all_reservations()

        return reservation_list_schema.dump(reservation).data, HTTPStatus.OK

    @jwt_required
    def post(self):
        json_data = request.get_json()
        current_user = get_jwt_identity()
        data, errors = reservation_schema.load(data=json_data)

        existing_reservations = Reservation.query.filter_by(time=json_data['time'], space_id=json_data['space_id'])
        if existing_reservations.count():
            return {'message': "A reservation already exists for given time and space"}, HTTPStatus.BAD_REQUEST

        if errors:
            return {'message': "Validation errors", 'errors': errors}, HTTPStatus.BAD_REQUEST
        reservation = Reservation(**data)
        reservation.user_id = current_user
        reservation.save()
        return reservation_schema.dump(reservation).data, HTTPStatus.CREATED


class ReservationResource(Resource):

    @jwt_optional
    def get(self, reservation_id):

        reservation = Reservation.get_by_id(reservation_id=reservation_id)

        if reservation is None:
            return {'message': 'reservation not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if reservation.user_id != current_user or current_user is None:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return reservation_schema.dump(reservation).data, HTTPStatus.OK

    @jwt_required
    def put(self, reservation_id):

        json_data = request.get_json()

        reservation = Reservation.get_by_id(reservation_id)

        if reservation is None:
            return {'message': 'reservation not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != reservation.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        reservation.id = json_data['id']
        reservation.time = json_data['time']

        reservation.save()

        return reservation.data(), HTTPStatus.OK

    @jwt_required
    def delete(self, reservation_id):

        reservation = Reservation.get_by_id(reservation_id)

        if reservation is None:
            return {'message': 'reservation not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != reservation.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        reservation.delete()

        return {}, HTTPStatus.NO_CONTENT

    @jwt_required
    def patch(self, reservation_id):
        json_data = request.get_json()

        data, errors = reservation_schema.load(data=json_data, partial=('name',))

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        reservation = Reservation.get_by_id(reservation_id=reservation_id)

        if reservation is None:
            return {'message': 'reservation not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != reservation.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        reservation.time = data.get('time') or reservation.time

        reservation.save()

        return reservation_schema.dump(reservation).data, HTTPStatus.OK


class ReservationUserResource(Resource):

    def get(self, user_id):
        reservation = Reservation.get_all_by_user_id(user_id=user_id)

        if reservation is None:
            return {'message': 'reservations not found'}, HTTPStatus.NOT_FOUND

        return reservation_list_schema.dump(reservation).data, HTTPStatus.OK


class ReservationSpaceResource(Resource):

    def get(self, space_id):
        reservation = Reservation.get_all_by_space_id(space_id=space_id)

        if reservation is None:
            return {'message': 'reservations not found'}, HTTPStatus.NOT_FOUND

        return reservation_list_schema.dump(reservation).data, HTTPStatus.OK
