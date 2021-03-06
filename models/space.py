from extensions import db


class Space(db.Model):
    __tablename__ = 'space'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer(), nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    @classmethod
    def get_by_id(cls, space_id):
        return cls.query.filter_by(id=space_id).first()

    @classmethod
    def get_by_capacity(cls, space_capacity):
        return cls.query.filter_by(capacity=space_capacity).all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_spaces(cls):
        return cls.query.all()
