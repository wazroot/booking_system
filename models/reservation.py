from extensions import db


class Reservation(db.Model):
    __tablename__ = 'reservation'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime(), nullable=False)
    user = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    space = db.Column(db.Integer(), db.ForeignKey('space.id'), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())