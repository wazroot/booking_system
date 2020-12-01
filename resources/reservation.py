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

