from extensions import db
from _datetime import datetime as dt

class Reservation(db.Model):
    __tablename__ = 'reservation'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Date(),
                     nullable=False)  # this datatype may need to be changed? How do we implement this on a query?
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    space_id = db.Column(db.Integer(), db.ForeignKey('space.id'), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())

    # updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())


    @classmethod
    def get_all_reservations(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, reservation_id):
        return cls.query.filter_by(id=reservation_id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def get_by_space(cls, space_id):
        return cls.query.filter_by(space_id=space_id).first()

    @classmethod
    def get_by_space_and_time(cls, space_id, time):
        # what time format are we going to use?
        return cls.query.filter_by(space_id=space_id, time=time).first()

    @classmethod
    def get_by_space_and_user(cls, user_id, space_id):
        return cls.query.filter_by(space=space_id, user=user_id).first()

    @staticmethod
    def convert_str_to_datetime(self, str_date):
        date_list = str.split(str_date, '/')

        date_datetime = dt(int(date_list[2]), int(date_list[1]), int(date_list[0]))

        return date_datetime.date()

