from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

#Create instance of SQLAlchemy
db = SQLAlchemy()
#Create instance of Marshmallow
ma = Marshmallow()
#Create instance of Bcrypt
bcrypt = Bcrypt()
#Create instance of JWT
jwt = JWTManager()