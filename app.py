
import os
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from Config import Config
from extensions import db, jwt
from resources.user import UserListResource, UserResource, MeResource, UserSpaceListResource
from resources.space import SpaceListResource, SpaceResource, SpaceCapacityResource
from resources.token import TokenResource, RefreshResource, RevokeResource, black_list
from resources.reservation import ReservationListResource, ReservationResource


def create_app():

    env = os.environ.get('ENV', 'Development')
    if env == 'Production':
        config_str = 'config.ProductionConfig'
    else:
        config_str = 'config.DevelopmentConfig'
    
    app = Flask(__name__)
    app.config.from_object(config_str)
    app.app_context().push()
    register_extensions(app)
    register_resources(app)
    return app

def register_extensions(app):

    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):

        jti = decrypted_token['jti']
        return jti in black_list


def register_resources(app):

    api = Api(app)
    api.add_resource(RefreshResource, '/refresh')
    api.add_resource(RevokeResource, '/revoke')
    api.add_resource(MeResource, '/me')
    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<string:username>')
    api.add_resource(TokenResource, '/token')
    
    api.add_resource(SpaceListResource, '/spaces')
    api.add_resource(SpaceResource, '/spaces/<int:space_id>')
    api.add_resource(SpaceCapacityResource, '/spaces/<int:space_capacity>')
    api.add_resource(UserSpaceListResource, '/users/<string:username>/spaces')
    
    api.add_resource(ReservationListResource, '/reservations')
    api.add_resource(ReservationResource, '/reservations/<int:reservation_id>')
    #api.add_resource(UserReservationListResource, '/users/<string:username>/reservations')
    

if __name__ == '__main__':
    
    app = create_app()
    app.run()
