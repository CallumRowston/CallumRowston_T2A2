from flask import Flask
from init import db, ma, bcrypt, jwt
from controllers.auth_controller import auth_bp
from controllers.cli_controller import db_commands
from controllers.canyon_controller import canyons_bp
from controllers.user_controller import users_bp
import os

def create_app():
    #Create Flask object
    app = Flask(__name__)

    #JSON sorting and environment variables
    app.config ['JSON_SORT_KEYS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    #Initialize instances within the app
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    #Home route for testing
    @app.route('/')
    def index():
        return 'Test Test Test'

    #Register Blueprints
    app.register_blueprint(db_commands)
    app.register_blueprint(auth_bp)
    app.register_blueprint(canyons_bp)
    app.register_blueprint(users_bp)

    # Error handling
    @app.errorhandler(404)
    def not_found(err):
        return {'error': str(err)}, 404

    #Basic test
    print('Hello Canyon')
    return app
    