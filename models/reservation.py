from extensions import db


class Reservation(db.Model):
    __tablename__ = 'reservation'

    id = db.Column(db.Integer(), primary_key=True)
    time = db.Column(db.Date(), nullable=False)
    user_id = db.Column(db.Integer())
    space_id = db.Column(db.Integer(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    

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
    def get_all_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_all_by_space_id(cls, space_id):
        return cls.query.filter_by(space_id=space_id).all()




