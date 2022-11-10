from flask import Blueprint, request, abort
from init import db, bcrypt
from datetime import date, timedelta
from models.user import User, UserSchema
from flask_jwt_extended import create_access_token, get_jwt_identity
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register/', methods=['POST'])
def register_user():
    data = UserSchema().load(request.json)
    try:
        user = User(
            name = data['name'],
            email = data['email'],
            password = bcrypt.generate_password_hash(data['password']).decode('utf-8')  
        )

        db.session.add(user)
        db.session.commit()

        return UserSchema(exclude=['password']).dump(user), 201

    except IntegrityError:
        return {'error': F'{user.email} already in use'}, 409

@auth_bp.route('/login/', methods=['POST'])
def login_user():

    # Query DB for matching email 
    stmt = db.select(User).filter_by(email=request.json['email'])
    user = db.session.scalar(stmt)

    # If user exists and password is correct then create token for user with 24hr time limit
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return {'email': user.email, 'token': token, 'is_admin': user.is_admin}
    else:
        return {'error': 'Invalid email or password'}, 401

def authorize_user():
    stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)

    if not user.is_admin:
        abort(401, description='Access denied. You are not an administrator')
