from models.reservation import Reservation
from schemas.validations import ReservationSchema
from flask import request
from flask_restful import Resource
from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional

# Tämä luokka toimii pääasiallisena rajapintana. Tänne metodit joilla tehdään varauksia ja etsitään varauksia käyttäjän id:llä,
# ja tilan id:llä

# Poistetaan täältä myöhemmin kaikki mitä ei tarvita.

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

        # get all reservations and make it a list
        all_reservations = Reservation.get_all_reservations()

        # if any reservations already exists for chosen space at a given time
        # give an error message, this might be useless as Aku has already put some validations for this.
        for i in range(0, (list(all_reservations).count(all_reservations)-1)):
            if all_reservations[i]["time"] == json_data['time'] and all_reservations[i]["space_id"] == json_data['space_id']:
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
        reservation.user_id = json_data['user_id']
        reservation.space_id = json_data['space_id']

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
