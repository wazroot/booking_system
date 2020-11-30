
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from Config import Config
from extensions import db, jwt
from resources.user import UserListResource, UserResource, MeResource, UserInstructionListResource
from resources.instruction import InstructionListResource, InstructionResource, InstructionPublic
from resources.token import TokenResource, RefreshResource, RevokeResource, black_list
# Muista muuttaa importit myöhemmin!!!


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.app_context().push()
    register_extensions(app)
    register_resources(app)
    return app

def register_extensions(app):
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)