from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

    db = SQLAlchemy(app)

    print('Hello Canyon')
    return app
    