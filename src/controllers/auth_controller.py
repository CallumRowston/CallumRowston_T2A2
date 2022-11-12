from flask import Blueprint, request, abort
from init import db, bcrypt
from datetime import timedelta
from models.user import User, UserSchema
from flask_jwt_extended import create_access_token, get_jwt_identity
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register/', methods=['POST'])
def register_user():
    # Register a user with username, email and password
    
    data = UserSchema().load(request.json)

    # Create a new user object if tje entered name and email do not already exist in the database
    # Also creates a hashed version of the users password for secure storage in the database
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
        return {'Error': F'{user.email} or {user.name} already in use'}, 409

@auth_bp.route('/login/', methods=['POST'])
def login_user():
    # Logs a user in if email and password are correct and provides a token with 24hr expiry

    # Query to get a user that has matching 'email' field to the email entered
    stmt = db.select(User).filter_by(email=request.json['email'])
    user = db.session.scalar(stmt)

    # If email and password match the user email and password in the database, provide an access token with 24hr expiry
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return {'email': user.email, 'token': token, 'is_admin': user.is_admin}

    return {'Error': 'Invalid email or password'}, 401

def authorize_user():
    # Grants or denies access to an admin-only route based on if the user is an admin or not

    # Query to return a user whose id matches the logged in user
    stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)

    # Checks if the selected users' is_admin field is False and aborts the action if so
    if not user.is_admin:
        abort(401, description='You must be an administrator to do that')
