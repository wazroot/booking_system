from models.reservation import Reservation

from flask import request
from flask_restful import Resource
from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional


#Tämä luokka toimii pääasiallisena rajapintana. Tänne metodit joilla tehdään varauksia ja etsitään varauksia käyttäjän id:llä,
#ja tilan id:llä

class ReservationListResource(Resource):

    def get(self):
        reservation = Reservation.get_by_id()

        pass
        #reservation_list_schema.dump(reservation).data, HTTPStatus.OK

    def post(self):
        pass


class ReservationResource(Resource):

    @jwt_optional
    def get(self, space_id):

        reservation = Reservation.get_by_id(reservation_id=reservation_id)

        if reservation is None:
            return {'message': 'reservation not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if reservation.is_publish == False and reservation.user_id != current_user:
        return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN                

        return reservation_schema.dump(reservation).data, HTTPStatus.OK

