from models.reservation import Reservation

from flask import request
from flask_restful import Resource
from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional


#Tämä luokka toimii pääasiallisena rajapintana. Tänne metodit joilla tehdään varauksia ja etsitään varauksia käyttäjän id:llä,
#ja tilan id:llä
reservation_schema = ReservationSchema()
reservation_list_schema = ReservationSchema(many=True)
class ReservationListResource(Resource):

    def get(self):
        reservation = Reservation.get_by_id()

        pass
        #reservation_list_schema.dump(reservation).data, HTTPStatus.OK

    def post(self):
        pass


class ReservationResource(Resource):

    @jwt_optional
    def get(self, reservation_id):

        reservation = Reservation.get_by_id(reservation_id=reservation_id)

        if reservation is None:
            return {'message': 'reservation not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if reservation.is_publish == False and reservation.user_id != current_user:
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

class ReservationPublic(Resource):
    @jwt_required
    def put(self, reservation_id):
        reservation = Reservation.get_by_id(reservation_id=reservation_id)

        if reservation is None:
            return {'message': 'reservation not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != reservation.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        reservation.is_publish = True
        reservation.save()

        return {}, HTTPStatus.NO_CONTENT

    @jwt_required
    def delete(self, reservation_id):
        reservation = Reservation.get_by_id(reservation_id=reservation_id)

        if reservation is None:
            return {'message': 'reservation not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != reservation.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        reservation.is_publish = False
        reservation.save()

        return {}, HTTPStatus.NO_CONTENT
